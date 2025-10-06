from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.Introduce, name='introduce'),
    path('troll/', views.Troll, name='troll'),
    path('register/', views.Register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name= 'page/login.html'), name= 'login'),
    path('logout/', auth_views.LogoutView.as_view(next_page= '/'), name= 'logout'),
]

 


