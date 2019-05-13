from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import UserCustomCreationForm
# Create your views here.

def index(request):
    return render(request, 'accounts/index.html')

def signup(request):
    if request.method =='POST':
        user_form = UserCustomCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            auth_login(request, user)
            return redirect('accounts:index')    
    else:
        user_form = UserCustomCreationForm()
        
    context = {'user_form':user_form}
    return render(request, 'accounts/signup.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('accounts:index')
        
    if request.method=='POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            return redirect('accounts:index')
    else:
        login_form = AuthenticationForm()
        
    context = {'login_form':login_form}
    
    return render(request, 'accounts/login.html', context)
    
@login_required
def logout(request):
    auth_logout(request)
    return redirect('accounts:index')
    
    