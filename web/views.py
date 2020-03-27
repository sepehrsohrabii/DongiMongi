from django.shortcuts import render
from django.http import JsonResponse
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from .models import User, Token, Expense, Person
from datetime import datetime


@csrf_exempt
def submit_person(request):
    """user submit an person"""

    this_name = request.POST['name']
    this_sahm = request.POST['sahm']


    Person.objects.create(name=this_name, sahm=this_sahm)

    return JsonResponse({
        'status': 'ok'
    }, encoder=JSONEncoder)


@csrf_exempt
def submit_expense(request):
    """user submit an expense"""

    this_token = request.POST['token']
    this_user = User.objects.filter(token__token=this_token).get()

    if 'date' not in request.POST:
        date = datetime.now()

    Expense.objects.create(user=this_user, amount=request.POST['amount'],
                           text=request.POST['text'], date=date)


    return JsonResponse({
        'status': 'ok'
    }, encoder=JSONEncoder)
