from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from .models import Movie, Genre, Director
from actors.models import Actor
from accounts.models import *
from accounts.forms import ScoreForm

# Create your views here.
# genre.json import 방법:
# $ python manage.py loaddata genre.json

def index(request):
    return render(request, 'movies/index.html')

def movie_lists(request):
    
    if not request.user.is_authenticated:
        return redirect("accounts:login")
        
    movies = Movie.objects.all()
    context = {'movies':movies}
    return render(request, 'movies/movies_list.html', context)
    
def movie_detail(request, movie_id):
    
    movie = get_object_or_404(Movie, pk=movie_id)
    
    if request.method=='POST':
        score_form = ScoreForm(request.POST)
        if score_form.is_valid() and request.POST.get('score'):
            score = score_form.save(commit=False)
            # 넘어 온 것 중 그것
            score.score = request.POST.get('score')
            score.movie = movie
            score.user = request.user
            score.save()
            for silmilar in request.user.me_similar.all():
                silmilar.add_movie(movie)
                silmilar.save()
            for silmilar in request.user.you_similar.all():
                silmilar.add_movie(movie)
                silmilar.save()
            
        return redirect('movies:movie_detail', movie_id)
                
    else:
        score_form = ScoreForm()

    context = {'movie':movie, 'score_form':score_form}
    return render(request, 'movies/movie_detail.html', context)
    
def genre_list(request):
    genres = Genre.objects.all()
    context = {'genres':genres}
    return render(request, 'movies/genres_list.html',context)
    
def genre_movies(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    context = {'genre':genre}
    return render(request, 'movies/genre_movies.html', context)
    
def director(request, director_id):
    director = get_object_or_404(Director, pk=director_id)
    context = {'director':director}
    return render(request, 'movies/director.html',context)

@login_required       
def movie_evaluate(request):
    movies = Movie.objects.all()
    context = {'movies':movies}
    return render(request, 'movies/movie_evaluate.html', context)
  
@login_required 
def delete_score(request, movie_id, score_id):
    score = get_object_or_404(Score, pk=score_id)
    movie = get_object_or_404(Movie, pk=movie_id)
    for silmilar in request.user.me_similar.all():
        silmilar.remove_movie(movie)
        silmilar.save()
    for silmilar in request.user.you_similar.all():
        silmilar.remove_movie(movie)
        silmilar.save()
    score.delete()
    return redirect('movies:movie_detail', movie_id)


def search_movie(request):
    movie_title = request.GET.get('search')   
    
    movie = Movie.objects.filter(title=movie_title)[0]
    
    print(movie)
    
    return redirect('movies:movie_detail', movie.id)

def search_movie2(request):
    
    return

'''
def search_movie2(request, movie_title):
    
    
'''


#------------------------------------------------
def out_movie(request):
    me = request.user
    
    out_len = 5
    out = []

    for movie in Movie.objects.all():
        if movie in me.score_set.all():
            continue
        
        man_score = 0.0
        for score in movie.score_set.all():
            temp = 0
            if Me_you_similar.objects.filter(me = me , you = score.user):
                temp = Me_you_similar.objects.filter(me = me , you = score.user)[0].silmilar
            elif Me_you_similar.objects.filter(me = score.user , you = me):
                temp = Me_you_similar.objects.filter(me = score.user , you = me)[0].silmilar
            temp *= score.score
            man_score += temp
                
        if man_score <= 0:
            continue
        if len(out)<out_len:
            out.append([movie,man_score])
        elif out[out_len-1][1] < man_score:
            out[out_len-1] = [movie,man_score]

        for i in range(len(out)-1,0,-1):
            if out[i][1] > out[i-1][1]:
                out[i] , out[i-1] = out[i-1] , out[i]
            else:
                break
    
    context={'out':out}
    return render(request, 'movies/out_movie.html', context)



