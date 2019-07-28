from django.urls import path
from django.conf.urls import url
from django.http import HttpResponse

from .views import home, login_, signup

urlpatterns = [
    path('login', login_, name='login'),
    path('signup', signup, name='signup'),
    path('home', home, name='home'),
]
