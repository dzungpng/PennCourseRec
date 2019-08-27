from django.urls import path
from django.conf.urls import url
from django.http import HttpResponse

from .views import (
    home, login_, signup, submit_description, save_description, recommendation, about
)

urlpatterns = [
    path('', login_, name='login'),
    path('signup', signup, name='signup'),
    path('home', home, name='home'),
    path('recommendation/submit/', submit_description, name='get-rec'),
    path('saved_descriptions', save_description, name = 'save'),
    path('recommendation/submit/saved_descriptions', save_description, name='save2'),
    path('courses_for_descriptions', recommendation, name = 'recommendation'),
    path('about', about, name='about')
]
