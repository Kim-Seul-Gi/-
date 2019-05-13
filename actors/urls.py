from django.urls import path
from . import views

app_name = 'actors'

urlpatterns = [
    path('', views.actors_list, name='actors_list'), 
    path('<int:actor_pk>/', views.actor_detail, name='actor_detail'), 
    path('prizes/', views.prizes_list, name='prizes_list'), 
]