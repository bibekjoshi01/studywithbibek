from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
   # path('join_room/<str:pk>/', views.join_group, name='join_room'),
    path('profile/<str:pk>/', views.userprofile, name='user-profile'),
    path('create_room/', views.create_room, name="create_room"),
    path('update_room/<str:pk>/', views.update_room, name="update_room"),
    path('delete_room/<str:pk>/', views.delete_room, name="delete_room"),
    path('login', views.loginpage, name="login"),
    path('logout', views.logoutuser, name="logout"),
    path('register', views.registeruser, name="register"),
    path('delete_message/<str:pk>/', views.delete_message, name="delete_message"),
    path('update_user', views.updateuser, name="update-user"),
    path('topics', views.topicspage, name="topics"),
    path('activity', views.activitypage, name="activity"),
    











]