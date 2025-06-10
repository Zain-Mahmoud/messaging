from django.urls import path, re_path
from . import views

from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login_view"),
    path("chats", views.chats, name="chats"),
    path("register", views.register_view, name="register_view"),
    path("newchat", views.newchat, name="newchat"),
    path("logout", views.logout_view, name="logout_view"),
    path("profile/<int:userid>", views.profile, name="profile"),
    #API routes
    path('getchats/<int:chatid>', views.get_chats, name="get_chats"),
    path('send/<int:chatid>', views.send, name="send"),
] 