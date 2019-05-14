from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from .forms import UserCustomCreationForm, UserCustomAuthenticationForm

from .models import Me_you_similar,Score
# Create your views here.

def index(request):
    return render(request, 'accounts/signin.html')

def signup(request):
    if request.method =='POST':
        print(request.POST)
        user_form = UserCustomCreationForm(request.POST)
        print(user_form)
        if user_form.is_valid():
            print("hello")
            user = user_form.save()
            #-------------------------------
            for you in get_user_model().objects.all():
                if you != user:
                    temp = Me_you_similar(me=user,you=you)
                    temp.first_update()
                    temp.save()
                
            #-------------------------------
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('movies:movie_index')    
    else:
        user_form = UserCustomCreationForm()
        
    context = {'user_form':user_form}
    return render(request, 'accounts/signup.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('accounts:index')
        
    if request.method=='POST':
        login_form = UserCustomAuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            return redirect('movies:movie_index')
    else:
        login_form = UserCustomAuthenticationForm()
        user_form = UserCustomCreationForm()
        
    context = {'login_form':login_form}
    
    return render(request, 'accounts/signin.html', context)
    
@login_required
def logout(request):
    auth_logout(request)
    return redirect('movies:movie_index')
    

    
    
    
