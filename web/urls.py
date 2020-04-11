from django.conf.urls import url
from . import views, forms

urlpatterns = [
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^q/generalstat/$', views.generalstat, name='generalstat'),
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^$', views.index, name='index'),
    url(r'^input/person/$', views.personinput, name='person_input'),
    url(r'^input/expense/$', views.expenseinput, name='expense_input')
]