from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name="user_login"),
    path('signup/', views.signup, name="signup"),
    path('home', views.home, name="home"),
    path('logout', views.logout, name="logout"),
    path('admin_login', views.admin_login, name="admin_login"),
    path('admin', views.admin_home, name='admin'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('adminlogout', views.adminlogout, name="adminlogout"),
    path('useradd',views.useradd, name="useradd" ),
    path('edit/<int:user_id>/', views.edit, name='edit'),
    path('search',views.user_search,name='search'),
    
]