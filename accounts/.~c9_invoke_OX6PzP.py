from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from .forms import UserCustomCreationForm, UserCustomAuthenticationForm

import random

from .models import Me_you_similar,Score
from movies.models import Movie
from actors.models import Actor
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
                    temp.update()
                    temp.save()
                
            #-------------------------------
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('movies:movie_evaluate')    
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
    
def profile(request,user_pk):
    User = get_user_model()
    user = get_object_or_404(User,pk=user_pk)
    
    if request.method=="POST" a:
        a = 1
    
    
    context = {'use':user}
    return render(request,'accounts/profile.html',context)

@login_required   
def follow(request,user_pk):
    User = get_user_model()
    user = get_object_or_404(User,pk=user_pk)
    me = request.user
    if user != me:
        if user in me.followers.all():
            me.followers.remove(user)
        else:
            me.followers.add(user)
    return redirect('accounts:profile',user_pk)
    
def create_profile(request, user_pk):
    # 뽑아와서 저장만 한다.
    for 
    print(request.POST)
    user = get_object_or_404(get_user_model(), pk=user_pk)
    genres = request.POST.get('genres')
    print(genres)
    return redirect('movies:movie_list')
    
@login_required
@require_POST
def edit_score(request,movie_pk,score_pk):
    score = Score.objects.get(pk = score_pk)
    movie = Movie.objects.get(pk = movie_pk)
    if score.score != request.POST.get('edit_score'):
        for silmilar in request.user.me_similar.all():
            silmilar.remove_movie(movie)
            silmilar.save()
        for silmilar in request.user.you_similar.all():
            silmilar.remove_movie(movie)
            silmilar.save()

        score.score = request.POST.get('edit_score')
        score.content = request.POST.get('edit_score_content')
        score.save()
        
        for silmilar in request.user.me_similar.all():
            silmilar.add_movie(movie)
            silmilar.save()
        for silmilar in request.user.you_similar.all():
            silmilar.add_movie(movie)
            silmilar.save()
    else:
        score.score = request.POST.get('edit_score')
        score.content = request.POST.get('edit_score_content')
        score.save()
            
    
    return redirect('movies:movie_detail',movie_pk)
    

# 관리자 모드 -----------------------------------
@login_required
def algorithm_clear(request):
    for model in Me_you_similar.objects.all():
        model.delete()
        
    users = get_user_model().objects.all()
    for idx in range(len(users)):
        for i in range(idx+1,len(users)):
            model = Me_you_similar(me = users[idx] , you = users[i])
            model.update()
            model.save()
    
    return render(request,'test/test_index.html')
    
@login_required
def make_bot(request):
    cnt = 0
    while cnt < 100:
        User = get_user_model()
        name = '__bot'+str(User.objects.count()+1)
        password = 'admin_bot'
        bot = User(username=name,password=password)
        print('bot :',end='')
        print(bot)
        bot.save()
        
        cnt+=1
    
    return redirect('accounts:test_algorithm_clear')
    
@login_required
def make_bot_score(request):
    idx = 0
    while idx < 100:
        idx+=1
        
        User = get_user_model()
        bots = User.objects.filter(username__startswith = '__bot')
        bot = bots[random.randint(0,len(bots)-1)]
        
        movies = list(Movie.objects.all())
        movie = movies[0]
        i = 0
        while i<len(movies):
            if movies[i].movie_scores.filter(user = bot):
                movies.remove(movies[i])
            else:
                i+=1
        
        if not(len(movies)):
            continue
                
        cut = min(100,len(movies)-1)
        movie = movies[random.randint(0,cut)]
    
        
        score_num = random.randint(1,10)
        content = 'maken by bot'
        
        score = Score(score=score_num , user=bot , movie=movie , content=content)
        score.save()
        
        for silmilar in bot.me_similar.all():
            silmilar.add_movie(movie)
        actor.save()
        for silmilar in bot.you_similar.all():
            silmilar.add_movie(movie)
            silmilar.save()

    return render(request,'test/test_index.html')
    
def search_sns(request,num):
    from bs4 import BeautifulSoup
    import requests
    
    actors = Actor.objects.all()#filter(pk=num)
    for actor in actors:
        name = str(actor.name)
        name = name.replace(' ','+')
        url = 'https://search.naver.com/search.naver?query={}'.format(name)
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        snss = soup.select('.detail_profile > dd > a')

        # out = ['url : {}'.format(url)]
        for sns in snss:
            text = sns.get('href')
            if 'twitter' in text:
                actor.twitter = text
                # out += ['twitter : {}'.format(actor.twitter)]
            elif 'facebook' in text:
                actor.facebook = text
                # out += ['facebook : {}'.format(actor.facebook)]
            elif 'instagram' in text:
                actor.instagram = text
                # out += ['instagram : {}'.format(actor.instagram)]
        actor.save()
    return render(request,'test/test_index.html')
    
