from django.contrib import admin
from .models import Game, StreamData, FavoriteGame, FavoriteStreamer

# Register your models here.
admin.site.register(Game)
admin.site.register(StreamData)
admin.site.register(FavoriteGame)
admin.site.register(FavoriteStreamer)