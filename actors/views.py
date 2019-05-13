from django.shortcuts import render, get_object_or_404
from .models import *

# Create your views here.
def actors_list(request):
    actors = Actor.objects.all()
    context={'actors':actors}
    return render(request,'actors/actors_list.html',context)
    
def prizes_list(request):
    prizes = Prize.objects.all()
    context={'prizes':prizes}
    return render(request,'actors/prizes_list.html',context)
    
def actor_detail(request, actor_pk):
    actor = get_object_or_404(Actor, pk=actor_pk)
    context={'actor':actor}
    return render(request,'actors/actor_detail.html',context)
    

