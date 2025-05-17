from django.shortcuts import render, get_object_or_404
from .utils import HEADERS, get_top_games, get_top_streams
from .models import Game
import requests

# Create your views here.
def home_view(request):

    games = get_top_games()
    streams = get_top_streams()
    if "data" in games:
        for game in games["data"]:
            game["box_art_url"] = game["box_art_url"].replace("{width}", "300").replace("{height}", "400")
            game["game_id"] = game["id"]

    if "data" in streams:
        for stream in streams["data"]:
            if "thumbnail_url" in stream:  # Some streams might use thumbnail_url
                stream["profile_image_url"] = stream["thumbnail_url"].replace("{width}", "300").replace("{height}", "400")
    

    return render(request, 'pages/home.html', {"games": games, "streams": streams})


#  individual games and streamers
def game_detail(request, game_id):
    game = get_object_or_404(Game, game_id = game_id)

    # Fetches streaming stats
    url = f"https://api.twitch.tv/helix/streams?game_id={game_id}"
    response = requests.get(url, headers=HEADERS)

    return render(request, "pages/game_detail.html", {"game": game})