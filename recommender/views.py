from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def home(request):
    return render(request, 'home.html', {})

def login_(request):
    if request.method =="POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
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
