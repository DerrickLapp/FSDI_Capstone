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
    game_id = models.CharField(max_length=255)
    viewer_count = models.IntegerField()
    start_time = models.DateTimeField()

    def __str__(self):
        return f"{self.streamer_id} streaming {self.game_id} at {self.start_time}"