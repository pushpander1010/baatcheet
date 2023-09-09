from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from .models import Room,RoomForm,Topic,Message
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.
def logoutUser(request):
    logout(request)
    return redirect('chat_app:home')

def registerUser(request):
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            return redirect('chat_app:login_register')
    context={'switch':'register','form':form}
    return render(request,'chat_app/login_register.html',context)


def login_register(request):
    context={'switch':'login'}
    if request.user.is_authenticated:
        return redirect('chat_app:home')

    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('chat_app:home')
        else :
            messages.error(request,"User is invalid")
            return redirect('chat_app:login_register')
    return render(request,'chat_app/login_register.html',context)

        

def home(request):
    q=request.GET.get('search') if request.GET.get('search') !=None else ''
    room=Room.objects.filter(Q(topic__name__icontains=q)| Q(discription__icontains=q) | Q(name__icontains=q))
    topics=Topic.objects.all()
    context={'rooms':room, 'topics':topics}
    return render(request,'chat_app/home.html',context)

def deleteMessage(request,id):
    message=Message.objects.get(id=id)
    if request.user==message.user:
        message.delete()
    else :
        messages.error(request,"You are not allowed to delete")
    return redirect('chat_app:room',id=message.room.id)

def editMessage(request,id):
    message=Message.objects.get(id=id)
    message.delete()
    return redirect('chat_app:room',id=message.room.id)


def room(request,id):
    room=Room.objects.get(id=id)
    participants=room.participants.all()
    if request.method=='POST':
        Message.objects.create(
            room=Room.objects.get(id=id),
            user=request.user,
            body=request.POST.get('addComment')
        )
        room.participants.add(request.user)
        return redirect('chat_app:room',id=room.id)
    roomMessages=room.message_set.all().order_by('-created')
    context={'rooms':room,'roomMessages':roomMessages,'participants':participants}
    return render(request,'chat_app/room.html',context)

@login_required(login_url='chat_app:login_register')
def createRoom(request):
    form=RoomForm(request.POST)
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('chat_app:home'))
        else:
            form=RoomForm(request.POST)
    context={'form':form}
    return render(request,'chat_app/createroom.html',context)

@login_required(login_url='chat_app:login_register')
def deleteRoom(request,id):
    room=Room.objects.get(id=id)
    if request.method=='POST':
        room=Room.objects.get(id=id)
        room.delete()
        return redirect('chat_app:home')
    return render(request,'chat_app/delete.html',{'rooms':room})

@login_required(login_url='chat_app:login_register')
def updateRoom(request,id):
    room=Room.objects.get(id=id)
    form=RoomForm(instance=room)
    if request.method=='POST':
        if request.user!=room.host:
            return HttpResponse("<h1>You are not allowed to edit this room</h1>")
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('chat_app:home')
    return render(request,'chat_app/updateRoom.html',{'form':form})


