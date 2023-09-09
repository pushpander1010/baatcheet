from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User


class Topic(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name
# Create your models here.
class Room(models.Model):
    host=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic=models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    participants=models.ManyToManyField(User,related_name='participants')
    name=models.CharField(max_length=200)
    discription=models.TextField(null=True,blank=True)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-updated','-created']

    def __str__(self) -> str:
        return self.name
    

class Message(models.Model):
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    body=models.TextField()
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.body[:50]
    
class RoomForm(ModelForm):
    class Meta:
        model=Room
        fields= '__all__'
