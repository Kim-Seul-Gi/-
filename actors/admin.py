from django.contrib import admin
from .models import Actor, Prize
# Register your models here.

class ActorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'imageurl','birthday')
admin.site.register(Actor, ActorAdmin)

class PrizeAdmin(admin.ModelAdmin):
    list_display = ('id','name','date')
admin.site.register(Prize, PrizeAdmin)