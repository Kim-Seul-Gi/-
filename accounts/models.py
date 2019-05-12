# accounts > models.py

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField # 필드 선언
from imagekit.processors import ResizeToFill    # 리사이징용

# Create your models here.

class User(AbstractUser):
    
    nickname     = models.CharField(max_length = 20)
    introduction = models.TextField()
    
    # 좋아하는 장르 3개
    like_genre_1 = models.CharField(max_length = 20)
    like_genre_2 = models.CharField(max_length = 20)
    like_genre_3 = models.CharField(max_length = 20)
    
    # 좋아하는 배우 3명
    like_actor_1 = models.CharField(max_length = 20)
    like_actor_2 = models.CharField(max_length = 20)
    like_acotr_3 = models.CharField(max_length = 20)
    
    # 유저 이미지
    image        = ProcessedImageField(
                        processors = [ResizeToFill(300, 300)],  # 잘라낼 사이즈
                        format = 'JPEG',                        # 이미지 포맷
                        options = {'quality' : 80},             # 품질
                )

    # 팔로잉 / 팔로워
    followers = models.ManyToManyField(
                        settings.AUTH_USER_MODEL,       # 자기 자신 넣어주기
                        related_name = 'followings'     # 상대방을 쉽게 참조하기 위해 
                )

