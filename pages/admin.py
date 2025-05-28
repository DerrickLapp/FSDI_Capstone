from django.contrib import admin
from .models import Game, StreamData, Favorite

# Register your models here.
admin.site.register(Game)
admin.site.register(StreamData)
admin.site.register(Favorite)