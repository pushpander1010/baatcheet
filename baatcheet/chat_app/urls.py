from django.urls import path
from . import views

app_name='chat_app'
urlpatterns=[
    path("",views.home,name='home'),
    path("room/<int:id>/",views.room,name='room'),
    path("create-room/",views.createRoom,name='createRoom'),
    path("delete-room/<int:id>/",views.deleteRoom,name='deleteRoom'),
    path("update-room/<int:id>/",views.updateRoom,name='updateRoom'),
]