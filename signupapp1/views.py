from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            msg = "Invalid username or password."
            return render(request, 'login.html', {'msg': msg})
    return render(request, 'login.html')

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            msg = "Username already taken"
            return render(request, 'signup.html',{'msg':msg})
        elif User.objects.filter(email=email).exists():
            msg = "Email is already taken"
            return render(request, 'signup.html',{'msg':msg})
        else:
            myuser = User.objects.create_user(username,email,password)
            myuser.save()
            return redirect('user_login')
    return render(request, 'signup.html' )

def home(request):
    return render(request, 'home.html')
