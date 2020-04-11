from django.db import models
from django.contrib.auth.models import User


class Passwordresetcodes(models.Model):
    code = models.CharField(max_length=32)
    email = models.CharField(max_length=120)
    time = models.DateTimeField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50) #TODO: do not save password


class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=48)
    def __str__(self):
        return "{}_token".format(self.user)


class Person(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=255)
    date = models.DateTimeField()
    amount = models.BigIntegerField()
    member = models.ManyToManyField(Person, through='Membership')
    def __str__(self):
        return "{}-{}-{}".format(self.user, self.text, self.amount)

class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    def __str__(self):
        return "{}-{}".format(self.person, self.expense)

class Manager(models.Model):
    manager = models.ForeignKey(Person, on_delete=models.CASCADE)
    managed_expense = models.OneToOneField(Expense, on_delete=models.CASCADE)
    def __str__(self):
        return "{}-{}".format(self.manager, self.managed_expense)

