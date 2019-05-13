from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from .models import Movie, Genre, Director
from actors.models import Actor
from accounts.models import *
# from accounts.forms import ScoreForm

# Create your views here.
# genre.json import 방법:
# $ python manage.py loaddata genre.json

def index(request):
    return render(request, 'movies/index.html')

def movie_lists(request):
    movies = Movie.objects.all()
    context = {'movies':movies}
    return render(request, 'movies/movies_list.html', context)
    
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    scores = movie.movie_scores.all()
    # score_form = ScoreForm()
    context = {'movie':movie, 'scores':score}
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

'''
@login_required
@request_POST
def create_score(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    
    new_score = Score()
    new_score

'''
@login_required       
def movie_evaluate(request):
  movies = Movie.objects.all()
  context = {'movies':movies}
  return render(request, 'movies/movie_evaluate.html', context)


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
            if Me_you_similar.objects.filter(me = me , you = score.user):
                temp = Me_you_similar.objects.filter(me = me , you = score.user)[0].silmilar
                temp *= score.score
                man_score += temp
        if man_score == 0:
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
    print(out)
    
    context={'out':out}
    
    return render(request, 'movies/out_movie.html', context)



