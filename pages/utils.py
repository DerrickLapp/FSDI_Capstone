from django.shortcuts import render
from .models import Game, StreamData
import os
import requests

CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
ACCESS_TOKEN = os.getenv("TWITCH_ACCESS_TOKEN")


HEADERS = {
    "Client-ID": CLIENT_ID,
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}



# trending games and streamers
def get_top_games():
    url = "https://api.twitch.tv/helix/games/top"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        games_data = response.json()["data"]
        for game in games_data:
            Game.objects.update_or_create(
                game_id=game["id"],
                defaults={
                    "name": game["name"],
                    "box_art_url": game["box_art_url"],
                }
            )
    return response.json()

def get_top_streams():
    url = "https://api.twitch.tv/helix/streams"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        streams_data = response.json()["data"]
        for stream in streams_data:
            StreamData.objects.update_or_create (
                user_id = stream["user_id"],
                defaults={
                "user_name":stream["user_name"],
                "title":stream["title"],
                "streamer_id":stream["id"],
                "game_id":stream["game_id"],
                "game_name":stream["game_name"],
                "viewer_count":stream["viewer_count"],
                "started_at":stream["started_at"],
                "thumbnail_url":stream["thumbnail_url"],
                "user_login":stream["user_login"],
                }
            )
    return response.json()


