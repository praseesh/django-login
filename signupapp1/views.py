from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model, login
from django.contrib.auth.hashers import check_password
from .forms import UserLoginForm
# from .models import CustomUser

User = get_user_model()

def user_login(request):   
    if 'email' in request.session:
         return redirect('home')      
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                user = User.objects.get(email=email)
                if check_password(password, user.password):
                    login(request, user)
                    request.session['email'] = email
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
    if 'email' in request.session:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('user_login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def home(request):
    if 'email' in request.session and request.user.is_authenticated :
        return render(request, 'home.html')
    
    return redirect('user_login')

def logout(request):
    if 'email'in request.session:
        request.session.flush()
    return redirect('user_login')

admin_username = 'admin'
admin_password = '1234'
def admin_login(request):
    if 'username' in request.session:
        return redirect('admin')
    if request.method == "POST":
        username = request.POST.get('admin1_username')
        password = request.POST.get('admin1_password')
        
        if username == admin_username and password == admin_password:
            request.session['username']=username 
            return redirect('admin')
        else:
            msg = "Invalid username or password."
            return render(request, 'adminlogin.html', {'msg': msg})
    return render(request, 'adminlogin.html')

def admin_home(request):
    if request.session is None:
        return redirect('admin_login')
    
    if request.method=='GET':
        users = User.objects.all()
        if users is not None:
            return render(request, 'admin.html', {'users': users})
        return render(request,'admin.html', {'users': 'The requested user is Empty'})
    
def delete_user(request, user_id):
    if request.method == 'DELETE':
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            # Return a JSON response indicating success
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            # Return a JSON response indicating failure due to non-existent user
            return JsonResponse({'success': False, 'error': 'User does not exist'})
    else:
        # Redirect to admin home if the request method is not DELETE
        return redirect('admin_home')