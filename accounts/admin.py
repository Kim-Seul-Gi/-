from django.contrib import admin
from .models import User
# Register your models here.

admin.site.register(User)


# 나중에 나오는지 확인해야한다.
# class ScoreAdmin(admin.ModelAdmin):
#     list_display = ('id', 'score', 'content', 'movie')
    
# admin.site.register(Score, ScoreAdmin)




