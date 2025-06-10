from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    profilepicture = models.ImageField(upload_to='profilepictures', default="")

    class Meta:
        swappable = 'AUTH_USER_MODEL'



class Chat(models.Model):
    starter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="startedchats")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receivedchats")
    lastmessage = models.CharField(default="")

class Message(models.Model):
    text = models.CharField()
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent")