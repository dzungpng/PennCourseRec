from django.utils import timezone

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import UpdateView

from .models import Course
from .forms import DescriptionSubmitForm

from .course_retrieval_engine import CourseRetrievalEngine

def home(request):
    # this is just a placeholder
    courses = Course.objects.filter(difficulty='3.00')[:6]
    return render(request, 'home.html', {'saved_courses': courses})


def login_(request):
    if request.method =="POST":
        user = authenticate(
            username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect("/home")
    return render(request, 'login.html', {})


def signup(request):
    #signup and authenticates user
    if request.method == "POST":
        user = User.objects.create_user(username=request.POST['username'],
                                        email=request.POST['email'],
                                        password=request.POST['password'])
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        login(request, user)
        return redirect("/home")
    return render(request, 'signup.html', {})


def logout_(request):
    logout(request)
    return redirect("/login")


def submit_description(request):
    """
    Makes a form for user to fill out their ideal course and submit
    to get recommendations.
    # """
    # form = DescriptionSubmitForm()
    # return render(request, 'submit_description.html', {'form': form})
    saved_courses = dict()
    if request.method == "POST":
        form = DescriptionSubmitForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.created_date = timezone.now()
            course.save()
            engine = CourseRetrievalEngine()
            recs = engine.query_similar_courses(course.description, 6)
            saved_courses = engine.view_recommendations(recs)
            print(saved_courses)
            #print(course.name)
            #print(course.description)
            #print(course.user)
            #print(course.created_date)
            #return redirect("/home", pk=course.pk) #this should be return render(request, 'home.html', {'recs': 'recs'})
            return render(request, 'home.html', {'saved_courses': saved_courses})
    else:
        form = DescriptionSubmitForm()
    return render(request, 'submit_description.html', {'form': form})
    # if request.method == "POST":
    #     print("On submit")
