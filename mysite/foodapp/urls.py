from django.urls import path
from . import views

urlpatterns = [
    path('foodadd/', views.Add_Dish, name='foodadd'),
    path('foodlist/', views.List_Dish, name='foodlist'),
    path('foodrandom/', views.Random_Dish, name='foodrandom'),
    path('test/', views.Test, name='test'),
]