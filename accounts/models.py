# accounts > models.py

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField # 필드 선언
from imagekit.processors import ResizeToFill    # 리사이징용
from movies.models import Movie, Genre
from actors.models import Actor

# Create your models here.

class User(AbstractUser):
    
    nickname     = models.CharField(max_length = 20)
    introduction = models.TextField()
    
    # 좋아하는 장르 3개
    like_genre_1 = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="genre_user_like_1", blank=True, null=True)
    like_genre_2 = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="genre_user_like_2", blank=True, null=True)
    like_genre_3 = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="genre_user_like_3", blank=True, null=True)
    
    # 좋아하는 배우 3명
    like_actor_1 = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name="actor_user_like_1", blank=True, null=True)
    like_actor_2 = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name="actor_user_like_2", blank=True, null=True)
    like_acotr_3 = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name="actor_user_like_3", blank=True, null=True)
    
    # 유저 이미지
    image        = ProcessedImageField(
                        processors = [ResizeToFill(300, 300)],  # 잘라낼 사이즈
                        format = 'JPEG',                        # 이미지 포맷
                        options = {'quality' : 80},             # 품질
                        blank=True
                )

    # 팔로잉 / 팔로워
    followers = models.ManyToManyField(
                        settings.AUTH_USER_MODEL,       # 자기 자신 넣어주기
                        related_name = 'followings'     # 상대방을 쉽게 참조하기 위해 
                )
    
    def __str__(self):
        return self.username
    
class Score(models.Model):
    
    score = models.IntegerField(blank=True)
    content = models.TextField()
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE, related_name="movie_scores")
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    
#--------------------------------------------------------------------

class Me_you_similar(models.Model):
    me = models.ForeignKey(User, on_delete = models.CASCADE, related_name='me_similar')
    my_sum_score = models.IntegerField(default = 0)
    you = models.ForeignKey(User, on_delete = models.CASCADE, related_name='you_similar')
    you_sum_score = models.IntegerField(default = 0)

    movie_sum = models.IntegerField(default = 0)
    same_genre_list = models.ManyToManyField(Genre,related_name='same_genre')
    silmilar = models.FloatField(default = 0.0)

    def add_movie(self,movie):
        if movie.score_set.filter(user = self.you) and movie.score_set.filter(user = self.me):
            my_score = movie.score_set.filter(user = self.me)[0]
            your_score = movie.score_set.filter(user = self.you)[0]
            self.my_sum_score += my_score**2
            self.you_sum_score += your_score**2
            self.movie_sum += my_score*your_score

            movie_similar = self.movie_sum/(self.my_sum_score*self.you_sum_score)**0.5
            self.silmilar = movie_similar+len(self.same_genre_list)*0.1

    def add_genre(self,genre):
        if genre in self.same_genre_list:
            return -1
        if genre.name != self.you.like_genre_1 and genre.name != self.you.like_genre_2 and genre.name != self.you.like_genre_3:
            return -1
        if genre.name != self.me.like_genre_1 and genre.name != self.me.like_genre_2 and genre.name != self.me.like_genre_3:
            return -1
        
        self.same_genre_list.add(genre)
        return 0
    
    def first_update(self):
        self.silmilar = self.movie_sum = self.you_sum_score = self.my_sum_score = 0
        for score in self.me.score_set.all():
            self.add_movie(score.movie)
    