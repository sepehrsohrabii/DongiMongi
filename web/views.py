# -*- coding: utf-8 -*-
import requests
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import User, Token, Expense, Person, Passwordresetcodes, Membership, Manager
from datetime import datetime
from django.template.response import TemplateResponse
import secrets
from django.core.mail import send_mail



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



def grecaptcha_verify(request):
    data = request.POST
    captcha_rs = data.get('g-recaptcha-response')
    url = "https://www.google.com/recaptcha/api/siteverify"
    params = {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': captcha_rs,
        'remoteip': get_client_ip(request)
    }
    verify_rs = requests.get(url, params=params, verify=True)
    verify_rs = verify_rs.json()
    return verify_rs.get("success", False)



def register(request):
    if 'requestcode' in request.POST: #form is filled. if not spam, generate code and save in db, wait for email confirmation, return message
        #is this spam? check reCaptcha
        if not grecaptcha_verify(request): # captcha was not correct
            context = {'message': 'کپچای گوگل درست وارد نشده بود. شاید ربات هستید؟ کد یا کلیک یا تشخیص عکس زیر فرم را درست پر کنید. ببخشید که فرم به شکل اولیه برنگشته!'} #TODO: forgot password
            return render(request, 'register.html', context)

        if User.objects.filter(email=request.POST['email']).exists(): # duplicate email
            context = {'message': 'متاسفانه این ایمیل قبلا استفاده شده است. در صورتی که این ایمیل شما است، از صفحه ورود گزینه فراموشی پسورد رو انتخاب کنین. ببخشید که فرم ذخیره نشده. درست می شه'} #TODO: forgot password
            return render(request, 'register.html', context)

        if not User.objects.filter(username=request.POST['username']).exists(): #if user does not exists
            code = secrets.token_hex(28)
            now = datetime.now()
            email = [request.POST['email']]
            password = make_password(request.POST['password'])
            username = request.POST['username']
            temporarycode = Passwordresetcodes(email=email, time=now, code=code, username=username, password=password)
            temporarycode.save()
            send_mail(subject='فعال سازی اکانت دنگی منگی',
                 from_email='sepehr0sohrabi@gmail.com',
                 recipient_list=email,
                 message='activation link: {}?email={}&code={}'.format(request.build_absolute_uri('/accounts/register/'), email, code)) #TODO: ye safheye login besazam ke ba in link mostaghim vared beshe
            context = {'message': "لینک فعالسازی برای شما ارسال شد."}
            return render(request, 'login.html', context)

        else:
            context = {'message': 'متاسفانه این نام کاربری قبلا استفاده شده است. از نام کاربری دیگری استفاده کنید.'} #TODO: forgot password
            #TODO: keep the form data
            return render(request, 'register.html', context)

    elif 'code' in request.GET: # user clicked on code
        email = request.GET['email']
        code = request.GET['code']
        if Passwordresetcodes.objects.filter(code=code).exists(): #if code is in temporary db, read the data and create the user
            new_temp_user = Passwordresetcodes.objects.get(code=code)
            newuser = User.objects.create(username=new_temp_user.username, password=new_temp_user.password, email=email)
            this_token = secrets.token_hex(48)
            token = Token.objects.create(user=newuser, token=this_token)
            Passwordresetcodes.objects.filter(code=code).delete() #delete the temporary activation code from db
            context = {'message': 'اکانت شما ساخته شد. توکن شما {} است.'.format(this_token)}
            return render(request, 'login.html', context)
        else:
            context = {'message': 'این کد فعال سازی معتبر نیست. در صورت نیاز دوباره تلاش کنید'}
            return render(request, 'login.html', context)
    else:
        context = {'message': ''}
        return render(request, 'register.html', context)




def login(request):

    if 'username' in request.POST and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        global this_user
        this_user = get_object_or_404(User, username=username)
        if (check_password(password, this_user.password)):  # authentication
            this_token = get_object_or_404(Token, user=this_user)
            global token
            token = this_token.token
            context = {}
            return redirect('/input/person/')
        else:
            context = {'message': 'نام کاربری یا کلمه عبور اشتباه بود'}
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html') #"accounts/login" ro ke hamun aval vared mikonim miad inja




@csrf_exempt
def personinput(request):
    this_user = User.objects.filter(token__token=token).get()
    person = Person.objects.filter(user=this_user)
    cont = {
        "object_list": person
    }
    if 'cancel' in request.POST:
        return redirect('/input/expense/')

    elif 'save' in request.POST:
        if request.POST['name']:
            this_user = User.objects.filter(token__token=token).get()
            this_name = request.POST['name']
            Person.objects.create(user=this_user, name=this_name)
        return render(request, 'personinput.html', cont)

    return render(request, 'personinput.html', cont)




@csrf_exempt
def expenseinput(request):
    person = Person.objects.filter(user=this_user)
    cont = {
        "object_list": person
    }

    if 'date' not in request.POST:
        date = datetime.now()

    if "cancel" in request.POST:
        return redirect('/q/generalstat/')

    elif "save" in request.POST:
        this_expense = Expense.objects.create(user=this_user, amount=request.POST['amount'],
                                              text=request.POST['text'], date=date)
        member = request.POST.getlist('member')
        manager = request.POST.getlist('manager')
        n = 0
        m = len(member) - 1
        for person.name in person:
            this_person = person.name
            if (n <= m) and (member[n] == str(this_person)):
                n = n + 1
                Membership.objects.create(person=this_person, expense=this_expense)
            if manager[0] == str(this_person):
                Manager.objects.create(manager=this_person, managed_expense=this_expense)
        return render(request, 'expenseinput.html')

    return render(request, 'expenseinput.html', cont)




@csrf_exempt
def generalstat(request):
    person = Person.objects.filter(user=this_user)
    expense = Expense.objects.filter(user=this_user)
    context = {}
    global args
    args = {}

    def MemberCounter(x):
        i = 0
        for person.name in x.member.all():
            i = i + 1
            print(i)
        return i

    for person.name in person:
        this_person = person.name
        print(this_person)
        this_money = 0
        for expense.text in expense:
            this_expense = expense.text
            print(this_expense)
            if this_person in this_expense.member.all():
                i = MemberCounter(this_expense)
                this_money = this_money + (int(str(this_expense.amount))/i)
                print(this_money)
                args.update({this_person: int(this_money)})
            if Manager.objects.filter(manager=this_person, managed_expense=this_expense).exists():
                this_money = this_money - int(str(this_expense.amount))
                args.update({this_person: int(this_money)})
    return TemplateResponse(request, 'generalstat.html', {'args':args})




def index(request):
    context = {}
    return render(request, 'index.html', context)
