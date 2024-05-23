from django.shortcuts import render, redirect
from django.contrib.auth.models import User
# from .models import CustomUser
# from django.contrib import messages
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model, login
from django.contrib.auth.hashers import check_password
from .forms import UserLoginForm

def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                user = User.objects.get(email=email)
                if check_password(password, user.password):
                    login(request, user)
                    return redirect('home')
                else:
                    msg = "Invalid email or password."
            except User.DoesNotExist:
                msg = "Invalid email or password."
            
            return render(request, 'login.html', {'form': form, 'msg': msg})
    else:
        form = UserLoginForm()
    
    return render(request, 'login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save the user object but don't commit to the database yet
            user.set_password(form.cleaned_data["password1"])  # This ensures the password is hashed
            user.save()  # Now save the user to the database
            login(request, user)  # Log the user in
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})
def home(request):
    return render(request, 'home.html')
