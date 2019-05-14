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
    
    # score 를 삭제하는 url입니다. score 생성은 movie_detail에서 다루고 있습니다.
    path('<int:movie_id>/delete_score/<int:score_id>/', views.delete_score, name="delete_score"), 
    
    # 추천하는 영화를 출력하는 url
    path('out_movie/', views.out_movie, name="out_movie"),
    
    # 전체 영화 리스트를 보여주고, 해당 영화의 이미지를 누르면 detail로 이동하게 됩니다.
    path('evaluate/', views.movie_evaluate, name="movie_evaluate"),
    
    
    # 김슬기가 190514 10시 45분 이후로 진행중인 url, 영화검색 누르면 해당 영화의 detail로 갑니다.
    path('search_movie/', views.search_movie, name='search_movie'),
    
    # 김슬기가 비동기 영화 검색을 하고자합니다 시무룩
    path('search_movie2/<str:movie_title>/', views.search_movie2, name="search_movie2"),
    
]