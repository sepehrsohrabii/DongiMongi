from django.db import models
from django.contrib.auth.models import User


class Expense(models.Model):
    text = models.CharField(max_length=255)
    date = models.DateTimeField()
    amount = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.IntegerField(null=False)
    def __str__(self):
        return "{}-{}".format(self.date, self.amount)

class Person(models.Model):
    name = models.CharField(max_length=255)
    sahm = models.IntegerField()
    def __str__(self):
        return "{}-{}".format(self.name, self.sahm)