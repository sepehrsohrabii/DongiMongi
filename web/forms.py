from django.forms import ModelForm
from .models import Person, Expense

class PersonInput(ModelForm):
    class Meta:
        model = Person
        exclude = ['name', 'money']

class ExpenseInput(ModelForm):
    class Meta:
        model = Expense
        exclude = ['text', 'amount', 'member']