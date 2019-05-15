from django.urls import path
from . import views

app_name='movies'

urlpatterns = [
    path('', views.index, name="movie_index"), 
    path('movielist/', views.movie_lists, name='movie_list'), ##
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'), 
    path('genre/', views.genre_list, name='genre_list'), 
    path('genre/<int:genre_id>/', views.genre_movies, name='genre_movies'), 
    path('director/<int:director_id>/', views.director, name='director'),
    
    # score 를 삭제하는 url입니다. score 생성은 movie_detail에서 다루고 있습니다.
    path('<int:movie_id>/delete_score/<int:score_id>/', views.delete_score, name="delete_score"), 
    
    # 추천하는 영화를 출력하는 url
    path('out_movie/', views.out_movie, name="out_movie"),
    
    # 첫 화면에서 review it 하면 전체 영화 리스트를 보여주고, 해당 영화의 이미지를 누르면 detail로 이동하게 됩니다.
    path('evaluate/', views.movie_evaluate, name="movie_evaluate"),
    
    # movie_list.html 에서 영화를 검색하면 해당 영화이름을 가지고 있는 영화들을 보여줍니다.
    path('search_movie/<str:movie_title>/', views.search_movie, name="search_movie"),
    
    #
    path('view_movies/<str:movie_title>', views.view_movies, name="view_movies"),
]