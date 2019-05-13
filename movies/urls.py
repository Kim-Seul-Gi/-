from django.urls import path
from . import views

app_name='movies'

urlpatterns = [
    path('', views.index, name="movie_index"), 
    path('movielist/', views.movie_lists, name='movie_list'), 
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'), 
    path('genre/', views.genre_list, name='genre_list'), 
    path('genre/<int:genre_id>/', views.genre_movies, name='genre_movies'), 
    path('director/<int:director_id>/', views.director, name='director'),
    
    path('out_movie/', views.out_movie, name="out_movie"),
    
    # 진행중입니다. 김슬기
    path('evaluate/', views.movie_evaluate, name="movie_evaluate"),
    # path('<int:movie_id>/create_score/', views.create_score, name="create_score"),
    
]