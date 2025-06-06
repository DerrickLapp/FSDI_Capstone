from django.contrib.auth.models import User
from django.db import models

# Create your models here.

# Game data
class Game(models.Model):
    name = models.CharField(max_length=255)
    game_id = models.CharField(max_length=255)
    box_art_url = models.URLField()

    def __str__(self):
        return self.name


# Stream Data for any specific streamer
class StreamData(models.Model):
    streamer_id = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    game_id = models.CharField(max_length=255)
    game_name = models.CharField(max_length=255)
    thumbnail_url = models.URLField()
    viewer_count = models.IntegerField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Streamer"
        verbose_name_plural = "Streamers"
        ordering = ["user_name", "started_at"]

    def __str__(self):
        return f"{self.user_name}"
    

# Favorites
class FavoriteGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorite_games = models.ForeignKey(Game, null=True, blank=True, related_name="favorite_games", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.favorite_games}"
    
class FavoriteStreamer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorite_streamers = models.ForeignKey(StreamData, null=True, blank=True, related_name="favorite_streamers", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.favorite_streamers.user_name}"