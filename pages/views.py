from django.shortcuts import render
from .utils import get_top_games, get_top_streams

# Create your views here.
def home_view(request):

    games = get_top_games()
    streams = get_top_streams()
    if "data" in games:
        for game in games["data"]:
            game["box_art_url"] = game["box_art_url"].replace("{width}", "300").replace("{height}", "400")

    if "data" in streams:
        for stream in streams["data"]:
            if "thumbnail_url" in stream:  # Some streams might use thumbnail_url
                stream["profile_image_url"] = stream["thumbnail_url"].replace("{width}", "300").replace("{height}", "400")
    

    return render(request, 'pages/home.html', {"games": games, "streams": streams})