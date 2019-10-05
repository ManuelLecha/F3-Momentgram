from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'Momentgram/init.html')

@login_required
def entry(reques):
    return render(request, 'Momentgram/entry.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username, email=email).exists():
            return HttpResponse("Username: " + username + " in use. Please try another one.")
        else:
            user = User.objects.create_user(username, email, password)
            return HttpResponse("Welcome to Momentgram, " + user.username)
    return render(request, 'Momentgram/register.html')

def signIn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username= username, password=password)


        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('entry'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
       
     
    return render(request, 'Momentgram/login.html')


