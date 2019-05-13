from django.shortcuts import render, get_object_or_404
from .models import Movie, Genre, Director
from actors.models import Actor
# Create your views here.
# genre.json import 방법:
# $ python manage.py loaddata genre.json
def lists(request):
    movies = Movie.objects.all()
    context = {'movies':movies}
    return render(request, 'movies/movie_list.html', context)
    
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    real_genres = movie.genres.all()
    context = {'movie':movie}
    return render(request, 'movies/movie_detail.html', context)
    
def genre_list(request):
    genres = Genre.objects.all()
    context = {'genres':genres}
    
    return render(request, 'movies/genre_list.html',context)
    
def genre_movies(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)

    context = {'genre':genre}

    return render(request, 'movies/genre_movies.html', context)
    
def actor_movies(request, actor_id):
    actor = get_object_or_404(Actor, pk=actor_id)
    print(actor)
    print(actor.movies.all())
    context = {'actor':actor}
    return render(request, 'movies/actor_movies.html', context)

def director(request, director_id):
    director = get_object_or_404(Director, pk=director_id)
    print(director)
    print(director.id)
    context = {'director':director}
    return render(request, 'movies/director.html',context)