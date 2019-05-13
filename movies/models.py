from django.db import models
# Create your models here.

# genre.json import 방법:
# $ python manage.py loaddata genre.json
class Genre(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name

class Director(models.Model):
    name = models.CharField(max_length=100)
    imageurl = models.CharField(max_length=100)
    birthday = models.CharField(max_length=40, blank=True)
    def __str__(self):
        return self.name
    
class Movie(models.Model):
    
    title = models.CharField(max_length=100)
    imageurl = models.CharField(max_length=100)
    director = models.ForeignKey(Director, blank=True, on_delete=models.CASCADE)
    release_date = models.CharField(max_length=20)
    overview = models.CharField(max_length=1000, default='')
    
    genres = models.ManyToManyField(Genre, related_name = 'genre_movies', blank=True)
    
    def __str__(self):
        return self.title