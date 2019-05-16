from django.contrib import admin
from .models import User, Score, Me_you_similar
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username','like_genre_1', 'like_genre_2', 'like_genre_3')
admin.site.register(User, UserAdmin)

# 나중에 나오는지 확인해야한다.
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'score', 'content', 'movie', 'user')
admin.site.register(Score, ScoreAdmin)

class Me_you_similarAdmin(admin.ModelAdmin):
    list_display = ('id','me','you','silmilar')
admin.site.register(Me_you_similar, Me_you_similarAdmin)





