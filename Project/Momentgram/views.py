from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Momentgram.models import Profile, Post, Follow
from datetime import datetime
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator
from .utils import *


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("timeline"))
    return render(request, 'Momentgram/init.html')

@login_required
def entry(request):
    return render(request, 'Momentgram/entry.html')

@login_required
def view_post(request, id=None):
    if id and getPost(id):
        post = getPost(id)
        context ={
            'username' : post.user.username,
            'description' : post.description,
            'image_name' : post.image,
            'date' : post.date
        }
        return render(request, 'Momentgram/post_visualization.html', context)
    return HttpResponse("No such post")


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name').split()
        l = len(name)
        name2=""
        for i in range(len(name)-1):
            name2 += " "+name[i+1]
        user = createUser(username, password, email, name[0], name2)
        if not user:
            return HttpResponse("Username: " + username + " or mail: " + email +  " in use. Please try another one.")
        else:
            return HttpResponseRedirect(reverse("login"))

    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("timeline"))
        return render(request, 'Momentgram/register.html')

def signIn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password = password)
        if user:
            login(request, user = user)
            if 'next' in request.session:
                next = request.session['next']
                request.session['next'] = None
                return redirect(next)
            return HttpResponseRedirect(reverse("timeline"))
        else:
            return HttpResponse("Failed. Username or password not correct")

    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("publish"))
        if request.GET.get('next',''):
            request.session['next'] = request.GET.get('next', '/')
        return render(request, 'Momentgram/login.html')

@login_required
def log_out(request):
    logout(request)
    return redirect('login')

@login_required
def publish_post(request):
    if request.method == 'POST':
        image_name = request.FILES['image'].name
        image = request.FILES['image']
        description = request.POST.get('description')
        post = createPost(description, request.user, image)
        context ={
            'username' : post.user.username,
            'description' : post.description,
            'image_name' : post.image,
            'date' : post.date
        }
        return render(request, 'Momentgram/post_visualization.html', context)
    if request.method == 'GET':
        return render(request, 'Momentgram/post.html')

@login_required
def show_profile(request, username, index = 1):
    user = getUser(username)
    if not user:
        return HttpResponse("That user doesn't exist: " + username)
    yourProfile = False
    followed = False
    if user.username == request.user.username:
        yourProfile = True
    else:
        if(request.user in getFollowers(user)):
            followed = True
    posts = getUserPosts(user)
    p = Paginator(posts, 9)
    maxPage = p.num_pages
    page = index
    context = {
         'followed' : followed,
         'yourProfile' : yourProfile,
         'username' : user.username,
         'n_posts' : len(getUserPosts(user)),
         'n_followed' : len(getFollowing(user)),
         'n_followers' : len(getFollowers(user)),
         'description' : (Profile.objects.filter(user=user)[0]).bio,
         'fullName' : user.first_name + " " + user.last_name,
         'posts' : p.page(page),
         'maxPage' : [ x+1 for x in range(maxPage)],
         'index' : index
    }
    return render(request, 'Momentgram/profile.html', context)


@login_required
def manage_friend(request, username, index = 1):
    user = getUser(username)
    if user:
        posts = getUserPosts(user)
        p = Paginator(posts, 9)
        maxPage = p.num_pages
        page = index
        if(user.username == request.user.username):
            context = {
                'yourProfile': True,
                'followed' : False,
                'username' : user.username,
                'n_posts' : len(getUserPosts(user)),
                'n_followed' : len(getFollowing(user)),
                'n_followers' : len(getFollowers(user)),
                'description' : (Profile.objects.filter(user=user)[0]).bio,
                'fullName' : user.first_name + " " + user.last_name,
                'posts' : p.page(page),
                'maxPage' : [ x+1 for x in range(maxPage)],
                'index' : index
            }
        else:
            followed = False
            if(request.user in getFollowers(user)):
                followed = True

            if(followed == True):
                unfollow(request.user,user)
                context = {
                    'yourProfile': False,
                    'followed' : not followed,
                    'username' : user.username,
                    'n_posts' : len(getUserPosts(user)),
                    'n_followed' : len(getFollowing(user)),
                    'n_followers' : len(getFollowers(user)),
                    'description' : (Profile.objects.filter(user=user)[0]).bio,
                    'fullName' : user.first_name + " " + user.last_name,
                    'posts' : p.page(page),
                    'maxPage' : [ x+1 for x in range(maxPage)],
                    'index' : index
                }
            else:
                follow(request.user, user)
                context = {
                    'yourProfile': False,
                    'followed' : not followed,
                    'username' : user.username,
                    'n_posts' : len(getUserPosts(user)),
                    'n_followed' : len(getFollowing(user)),
                    'n_followers' : len(getFollowers(user)),
                    'description' : (Profile.objects.filter(user=user)[0]).bio,
                    'fullName' : user.first_name + " " + user.last_name,
                    'posts' : p.page(page),
                    'maxPage' : [ x+1 for x in range(maxPage)],
                    'index' : index
                }
        return render(request, 'Momentgram/profile.html', context)
    else:
        return HttpResponse("No such user")


def search_users(request, isProfile='0', searched ="", index = 1):
    if 'searched' in request.GET:
        searched = request.GET.get('searched')
    sorted = getUsersSorted(request.user, searched)
    users = [x.username for x in sorted if x.username != request.user.username]
    p = Paginator(users, 9)
    maxPage = p.num_pages
    page = index
    if isProfile=='1':
        context = {
            'users' : p.page(page),
            'maxPage' : [ x+1 for x in range(maxPage)],
            'searched' : searched,
            'isProfile' : isProfile
        }
    else:
        context = {
            'users' : p.page(page),
            'maxPage' : [ x+1 for x in range(maxPage)],
            'searched' : searched
        }

    return render(request, 'Momentgram/searchUsers.html', context)

def timeline(request, index = 1):
    if request.method == "GET":
        posts = getTimeline(request.user)
        p = Paginator(posts, 9)
        print(p.num_pages)
        maxPage = p.num_pages
        context = {
            'posts' : p.page(index),
            'maxPage' : [ x+1 for x in range(maxPage)],
            'index' : index
        }
        return render(request, 'Momentgram/timeline.html', context)

def chat( request, username=""):
    if username:
        if( request.method == 'GET' ):
            user = getUser(username)
            messages = getChat(request.user, user)
            if(len(messages)>30):
                start = len(messages) - 30
            else:
                start = 0

            context = {
                'username' : username,
                'messages' : messages[start:]
            }
            return render(request,'Momentgram/chat.html', context)
        if ( request.method == 'POST' ):
            if 'message' in request.POST :
                        message = request.POST.get('message')
            user = getUser(username)
            if message:
                sendMessage(request.user,user,message)
            messages = getChat(request.user, user)
            if(len(messages)>30):
                start = len(messages) - 30
            else:
                start = 0
            context = {
                'username' : username,
                'messages' : messages[start:]
            }
            return render( request, 'Momentgram/chat.html', context)
    else:
        return HttpResponse("No such user")



