from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^submit/expense/$', views.submit_expense, name='sumbit_expense'),
    url(r'^submit/person/$', views.submit_person, name='sumbit_person'),
    url(r'^accounts/register/$', views.register, name='register'),
]