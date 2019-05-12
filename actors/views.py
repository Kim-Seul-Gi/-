from django.shortcuts import render, get_object_or_404
from .models import *

# Create your views here.
def list_actors(request):
    actors = Actor.objects.all()
    return render(request,'actors/list_actors.html',{'actors':actors})
    
def list_prizes(request):
    prizes = Prize.objects.all()
    return render(request,'actors/list_prizes.html',{'prizes':prizes})
    
def detail_actor(request,actor_pk):
    actor = get_object_or_404(Actors,pk=actor_pk)
    return render(request,'actors/detail_actor.html',{'actor':actor})
    

