from django.urls import path
from .import views

urlpatterns = [
    path('', views.user_login, name="user_login"),
    path('signup/', views.signup, name="signup"),
    path('home/', views.home, name="home" )
]