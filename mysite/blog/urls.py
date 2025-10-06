from django.urls import path, include
from . import views
from .views import Post_Create, Blog_List, PostViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'posts', PostViewSet)


urlpatterns = [
    path('list/', Blog_List.as_view(), name='bloglist'),
    path('page/', views.Blog_Page, name='blogpage'),
    path('mypage/', views.Blog_My_Page, name='blogmypage'),
    path('authorpage/<int:pk>/', views.Blog_Author_Page, name='blogauthorpage'),
    path('create/', Post_Create.as_view(), name='postcreate'),  
    path('update/<int:pk>/', views.Post_Update, name='postupdate'),
    path('api/', include(router.urls), name='apiroot'), 
    path('chat/', views.Blog_Chat, name='blogchat'),
]

 

