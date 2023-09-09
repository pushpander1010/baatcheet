from django.urls import path
from . import views

app_name='chat_app'
urlpatterns=[
    path("",views.home,name='home'),
    path("room/<str:id>/",views.room,name='room'),
    path("create-room/",views.createRoom,name='createRoom'),
    path("delete-room/<str:id>/",views.deleteRoom,name='deleteRoom'),
    path("update-room/<str:id>/",views.updateRoom,name='updateRoom'),
    path("logoutUser",views.logoutUser,name='logoutUser'),
    path("login_register",views.login_register,name='login_register'),
    path("registerUser",views.registerUser,name='registerUser'),
    path("deleteMessage/<str:id>/",views.deleteMessage,name='deleteMessage'),
    path("editMessage/<str:id>/",views.editMessage,name='editMessage'),
]