from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from .utils import HEADERS, get_top_games, get_top_streams
from .models import Game, StreamData
from .forms import ContactForm
from django.core.mail import send_mail
import requests

# Create your views here.
def home_view(request):

    games = get_top_games()
    streams = get_top_streams()
    form = ContactForm()

    if "data" in games:
        for game in games["data"]:
            game["box_art_url"] = game["box_art_url"].replace("{width}", "300").replace("{height}", "400")
            game["game_id"] = game["id"]
            

    if "data" in streams:
        for stream in streams["data"]:
            stream["streamer_id"] = stream["id"]
            stream["user_name"] = stream["user_name"]
            stream["user_id"] = stream["user_id"]
            stream["title"] = stream["title"]
            stream["game_id"] = stream["game_id"]
            stream["game_name"] = stream["game_name"]
            stream["viewer_count"] = stream["viewer_count"]
            stream["started_at"] = stream["started_at"]

            if "thumbnail_url" in stream:  # Some streams might use thumbnail_url
                stream["profile_image_url"] = stream["thumbnail_url"].replace("{width}", "300").replace("{height}", "400")


    if request.method == "POST":
        form = ContactForm(request.POST)
        #collect the data of the form
        if form.is_valid():
            print("Data is Valid")

            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            # This is the email information
            message_body = (
                f"You have a new email from DTTW \n"
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Message: {message}"
            )

            #Try to send the email! 
            try:
                #send_mail <-- Django Core Email
                send_mail(
                    "Email from DTTW",      #Subject
                    message_body,                #Message Body -> What the user typed in message
                    email,                       #From email -> The user's email
                    ['derrickelapp@hotmail.com'] #To Email -> Where you want to get the email message
                )

                print("Email sent successfully")
                #Render and redirect user
                return redirect("home")

            except Exception as e:
                #catching malicious behavior
                print(f"Error sending the email:{e}")

                return render(request, 'pages/home.html', {
                    "games": games,
                    "streams": streams,
                    "form":form,
                    "error":str(e)
                })
                
        else:
            print("Data is NOT Valid")
    else:
        #There is not POST request
        form = ContactForm()
    form = ContactForm()
                    
    return render(request, 'pages/home.html', {"games": games, "streams": streams, "form": form})


#  individual games and streamers
def game_detail(request, game_id):
    game = get_object_or_404(Game, game_id = game_id)
    game.box_art_url = game.box_art_url.replace("{width}", "300").replace("{height}", "400")
    
    # Fetches streaming stats
    url = f"https://api.twitch.tv/helix/streams?game_id={game_id}"
    response = requests.get(url, headers=HEADERS)
    streams = []

    if response.status_code == 200:
        data = response.json().get("data", [])

        for stream in data:
            streams.append({
                "user_name": stream["user_name"],
                "title": stream["title"],
                "viewer_count": stream["viewer_count"],
                "started_at": stream["started_at"],
                "url": f"https://www.twitch.tv/{stream['user_name']}"
            })

    return render(request, "pages/game_detail.html", {"game": game, "streams": streams})


def streamer_detail(request, user_id):
    streamer = get_object_or_404(StreamData, user_id = user_id)
    streamer.thumbnail_url = streamer.thumbnail_url.replace("{width}", "300").replace("{height}", "400")

    # Fetches streaming stats
    url =f"https://api.twitch.tv/helix/streams?user_id={user_id}"
    response = requests.get(url, headers=HEADERS)

    # Fetching past videos
    videos_url = f"https://api.twitch.tv/helix/videos?user_id={user_id}"
    videos_response = requests.get(videos_url, headers=HEADERS)
    videos_data = videos_response.json().get("data", [])
    print(videos_data)
    

    for video in videos_data:
        if "thumbnail_url" in video:
            video["thumbnail_url"] = video["thumbnail_url"].replace("%{width}", "300").replace("%{height}", "400")
    

    return render(request, "pages/streamer_detail.html", {"streamer": streamer, "videos_data": videos_data})


# Contact View
def contact_view(request):
    
    return render(request, 'pages/contact.html', {})