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
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name


class Expense(models.Model):
    text = models.CharField(max_length=255)
    date = models.DateTimeField()
    amount = models.BigIntegerField()
    user = models.ManyToManyField(Person, related_name='person2person')
    number = models.IntegerField(null=True)
    def __str__(self):
        return "{}-{}-{}".format(self.date, self.user, self.amount)

class MadarKharj(models.Model):
    madarrrrr = models.OneToOneField(Person, related_name='Madar_Kharj', on_delete=models.CASCADE)
    kharj = models.OneToOneField(Expense, related_name='Kharj', on_delete=models.CASCADE)


