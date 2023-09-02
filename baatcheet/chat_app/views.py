from django.shortcuts import render,redirect
from django.urls import reverse
from .models import Room,RoomForm,Topic
from django.db.models import Q

# Create your views here.
def home(request):
    q=request.GET.get('search') if request.GET.get('search') !=None else ''
    room=Room.objects.filter(Q(topic__name__icontains=q)| Q(discription__icontains=q) | Q(name__icontains=q))
    topics=Topic.objects.all()
    context={'rooms':room, 'topics':topics}
    return render(request,'chat_app/home.html',context)

def room(request,id):
    room=Room.objects.get(id=id)
    context={'rooms':room}
    return render(request,'chat_app/room.html',context)

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

def deleteRoom(request,id):
    room=Room.objects.get(id=id)
    if request.method=='POST':
        room=Room.objects.get(id=id)
        room.delete()
        return redirect('chat_app:home')
    return render(request,'chat_app/delete.html',{'rooms':room})

def updateRoom(request,id):
    room=Room.objects.get(id=id)
    form=RoomForm(instance=room)
    if request.method=='POST':
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('chat_app:home')
    return render(request,'chat_app/updateRoom.html',{'form':form})


