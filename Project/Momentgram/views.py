from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Momentgram.models import Profile



def index(request):
    return render(request, 'Momentgram/init.html')

@login_required
def entry(request):
    return render(request, 'Momentgram/entry.html')


def register(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists() or User.objects.filter(email = email).exists():
            return HttpResponse("Username: " + username + "or mail: " + email +  " in use. Please try another one.")
        else:
            user = User.objects.create_user(username, email, password)
            return HttpResponse("Welcome to Momentgram, " + user.username)

    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponse("You are already registered and logged in using: ") #+ request.user.username)
            # if init page is done, send him there
        return render(request, 'Momentgram/register.html')

def signIn(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password = password)
        if user:
            login(request, user = user)
            if(request.session['next']):
                next = request.session['next']
                request.session['next'] = None
                return redirect(next)
            return HttpResponse("logged in")
        else:
            return HttpResponse("Failed. Username or password not correct")

    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponse("You are already logged in using: "+request.user.username)
            # if init page is done, send him there
        if request.GET.get('next',''):
            request.session['next'] = request.GET.get('next', '/')
        return render(request, 'Momentgram/login.html')

def log_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')





