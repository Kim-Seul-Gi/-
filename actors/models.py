from django.db import models
from django.conf import settings
from movies.models import Genre, Movie

# Create your models here.
class Actor(models.Model):
    name = models.CharField(max_length=100) #김슬기가 가져올 수 있음
    image = models.ImageField(blank=True) #김슬기가 가져올 수 있음
    twitter = models.CharField(max_length=100,blank=True)
    instagram = models.CharField(max_length=100,blank=True)
    facebook = models.CharField(max_length=100,blank=True)
    birthday = models.CharField(max_length=40,blank=True) #김슬기가 가져올 수 있음
    movies = models.ManyToManyField(Movie,related_name="movie_actors",blank=True) #김슬기가 가져올 수 있음
    
    def __str__(self):
        return 'Actor name : {}'.format(self.name)



class Prize(models.Model):
    name = models.CharField(max_length=100)
    actors = models.ManyToManyField(Actor,related_name="actor_prizes",blank=True)
    movies = models.ManyToManyField(Movie,related_name="movie_prizes",blank=True)
    date = models.CharField(max_length=40,blank=True)
    
    def __str__(self):
        return 'Prize name : {}'.format(self.name)