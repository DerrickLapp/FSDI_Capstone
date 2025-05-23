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
    streamer_id = models.CharField(max_length=255, unique=True)
    user_name = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    game_id = models.CharField(max_length=255)
    game_name = models.CharField(max_length=255)
    thumbnail_url = models.URLField()
    viewer_count = models.IntegerField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user_name} streaming {self.game_name} at {self.started_at}"