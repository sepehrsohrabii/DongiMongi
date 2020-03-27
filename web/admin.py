from django.contrib import admin
from .models import Expense, Person, Token

admin.site.register(Expense)
admin.site.register(Person)
admin.site.register(Token)
