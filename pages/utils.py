import os
import requests

CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
ACCESS_TOKEN = os.getenv("TWITCH_ACCESS_TOKEN")

HEADERS = {
    "Client-ID": CLIENT_ID,
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

def get_top_games():
    url = "https://api.twitch.tv/helix/games/top"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def get_top_streams():
    url = "https://api.twitch.tv/helix/streams"
    response = requests.get(url, headers=HEADERS)
    return response.json()