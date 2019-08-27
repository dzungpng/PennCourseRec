from django.utils import timezone

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import UpdateView

from .models import Course, SavedDescription
from .forms import DescriptionSubmitForm

from .course_retrieval_engine import CourseRetrievalEngine


def home(request):
    # this is just a placeholder
    courses = Course.objects.filter(difficulty='3.00')[:6]
    return render(request, 'home.html', {'saved_courses': courses})


def about(request):
    """
    Appears when click on 'PennCourseRec' title.

    :param request:
    :return: None.
    """
    return render(request, 'about.html')


def login_(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect("/home")
    return render(request, 'login.html', {})


def signup(request):
    # signup and authenticates user
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

    """
    # global saved_courses
    saved_courses = dict()
  
    if request.method == "POST":
        form = DescriptionSubmitForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            request.session['description'] = course.description
            request.session['name'] = course.name
            course.user = request.user
            course.created_date = timezone.now()
            course.save()
            engine = CourseRetrievalEngine()
            recs = engine.query_similar_courses(course.description, 6)
            saved_courses = engine.view_recommendations(recs)
            request.session['saved_courses'] = saved_courses
            return render(request, 'home.html', {'saved_courses': saved_courses})
    else:
        form = DescriptionSubmitForm()
    return render(request, 'submit_description.html', {'form': form})
    # if request.method == "POST":
    #     print("On submit")


def save_description(request):
    # save the description
    if request.method == "POST":
        saved_description = SavedDescription.objects.create(user=request.user,
                                                            description=request.session['description'],
                                                            name=request.session['name'])
        # saved_description.course.clear()
        for course in request.session['saved_courses']:
            print(course)
            print(type(course))
            attached_course = Course.objects.get(name = course['name'])
            saved_description.course.add(attached_course)
    all_saved_descriptions = SavedDescription.objects.all()
    return render(request, 'saved_description.html', {'all_saved_descriptions' : all_saved_descriptions})


def recommendation(request):
    # get the list of courses attached to a certain saved description
    description = SavedDescription.objects.get(id=request.GET["id"])
    courses = description.course.all()
    return render(request, "courses.html", {"courses": courses})


