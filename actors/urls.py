from django.urls import path
from . import views

app_name = 'actors'

urlpatterns = [
    path('', views.list_actors, name='actors_list'), 
    path('<int:actor_pk>/', views.detail_actor, name='actor_detail'), 
    path('prizes/', views.list_prizes, name='prizes_list'), 
]