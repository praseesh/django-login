
 from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model, login
from django.contrib.auth.hashers import check_password
from .forms import UserLoginForm
from django.views.decorators.cache import never_cache
from .models import CustomUser

User = get_user_model()
admin_username = 'admin'
admin_password = '1234'

  


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

def admin_login(request):
    if 'username' in request.session:
        return redirect('admin')
    if request.method == "POST":
        username = request.POST.get('admin1_username')
        password = request.POST.get('admin1_password')
        if username==admin_username and password==admin_password:
            request.session['username']=username 
            return redirect('admin')
        else:
            msg = "Invalid username or password."
            return render(request, 'adminlogin.html', {'msg': msg})
    return render(request, 'adminlogin.html')

def admin_home(request):
    if 'username' in request.session:
        if request.method == 'GET':
            users = CustomUser.objects.all()
            return render(request, 'admin.html', {'users': users})
    return redirect('admin_login')

def delete_user(request, user_id):
    if request.method == 'POST':  
        try:
            user = get_object_or_404(CustomUser, id=user_id)
            user.delete()
            return redirect('admin') 
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User does not exist'})
    return redirect('admin')
    
def adminlogout(request):
    if 'username' in request.session:
        request.session.flush()
    return redirect('admin_login')

def edit(request,user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin')
    else:
        form = CustomUserCreationForm(instance=user)
    return render(request, 'edit.html', {'form': form, 'user': user})
    
def useradd(request):
    if 'username' in request.session:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()  
                return redirect('admin_login')
        else:
            form = CustomUserCreationForm()
    return render(request, 'useradd.html', {'form': form})

def user_search(request):
    search_query = request.GET.get('search')
    users = User.objects.filter(username__icontains=search_query) if search_query else User.objects.all()
    return render(request, 'admin.html', {'users': users, 'search_query': search_query})


