from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django import forms


# Create your views here.
def index(request):
    return render(request, "messaging/index.html")

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        v1 = User.objects.filter(username=username).first()
        v2 = User.objects.filter(password=password)
        valid = v1 in v2
        if valid:
            login(request, v1)
            return HttpResponseRedirect(reverse(chats))
        else:
            return render(request, "messaging/login.html", {
                'verified': False
            })    

    return render(request, "messaging/login.html", {
        "verfied": True
    })

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse(index))

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST['password']
        fname = request.POST['fname']
        lname = request.POST['lname']
        repeat = request.POST['repeat']
        email = request.POST['email']
        pfp = request.FILES['image']
        if User.objects.filter(username=username).exists():
            return render(request, "messaging/register.html", {
                "passwords_match": True,
                "userclash": True
            })
        elif repeat != password:
            return render(request, "messaging/register.html", {
                "passwords_match": False,
                "userclash": False
            }) 
        elif User.objects.filter(email=email).exists():
            return render(request, "messaging/register.html", {
                "userclash": True,
                "passwords_match": True,
            })
        else:
            new_user = User(username=username, password=password, first_name=fname, last_name=lname, email=email, profilepicture=pfp)
            new_user.save()
            return HttpResponseRedirect(reverse(login_view))

    return render(request, "messaging/register.html", {
        "passwords_match": True,
        "userclash": False
    })

@login_required
def newchat(request):
    if request.method == 'POST':
        recipient_username = request.POST['recipient']
        message = request.POST['message']
        try: 
            recipient = User.objects.get(username=recipient_username)
            if recipient == request.user:
                return render(request, 'messaging/newchat.html', {
                    'verified': True,
                    'different': False,
                    'exists': False
                })
            if Chat.objects.filter(starter=recipient).filter(receiver=request.user).exists() or Chat.objects.filter(receiver=recipient).filter(starter=request.user):
                return render(request, 'messaging/newchat.html', {
                'verified': True,
                'different': True,
                'exists': True
                })
            new_chat = Chat(starter=request.user, receiver=recipient, lastmessage=message)
            new_chat.save()
            message = Message(text=message, chat=new_chat, author=request.user)
            message.save()
            return HttpResponseRedirect(reverse(chats))
        except:
            return render(request, 'messaging/newchat.html', {
                'verified': False,
                'different': True,
                'exists': False
            })

    return render(request, "messaging/newchat.html", {
        'verified': True,
        'different': True,
        'exists': False
    })

@login_required
def chats(request):

    return render(request, "messaging/chats.html", {
        "chats": request.user.startedchats.all().union((request.user.receivedchats.all()))
    })

@login_required
def get_chats(request, chatid):
    chat = Chat.objects.get(id=chatid)
    messages = chat.messages.all()

    data = {'messages':[ (message.text, message.author.username, message.author.first_name) for message in messages]}
    return JsonResponse(data)

@login_required
def send(request, chatid):
    if request.method == 'POST':
        user = request.user
        message = request.POST['message']
        chat = Chat.objects.get(id=chatid)
        new_message = Message(text=message, chat=chat, author=user)
        new_message.save()
    return HttpResponseRedirect(reverse(chats))

@login_required
def profile(request, userid):
    userprofile = User.objects.get(id=userid)
    if request.user != userprofile:
        return HttpResponseRedirect(reverse(request, kwargs={'userid': request.user.id}))
    return render(request, "messaging/profile.html")
    