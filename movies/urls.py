from django.urls import path
from . import views

app_name='movies'

urlpatterns = [
    path('', views.lists, name='movie_list'),
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('genre/', views.genre_list, name='genre_list'),
    path('genre/<int:genre_id>', views.genre_movies, name='genre_movies'),
    path('actor/<int:actor_id>', views.actor_movies, name='actor_movies'),
    path('director/<int:director_id>', views.director, name='director'),
]