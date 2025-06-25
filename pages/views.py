from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from datetime import timedelta
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from .utils import HEADERS, get_top_games, get_top_streams
from .models import Game, StreamData, FavoriteGame, FavoriteStreamer
from .forms import ContactForm
import requests, json

# Create your views here.
def home_view(request):
    # If last fetched time is > 1 minute, get top games and streams
    latest_entry = Game.objects.order_by('-fetched_at').first()

    if not latest_entry or now() - latest_entry.fetched_at > timedelta(minutes=1):
        get_top_games()
        get_top_streams()

    # Gets 20 most recent entries in the database
    recent_games = Game.objects.order_by("-fetched_at")[:20]
    recent_streams = StreamData.objects.order_by("-fetched_at")[:20]

    # Gets the Contact Form
    form = ContactForm()


    # Gets the data from the database to present to HTML
    for game in recent_games:
        game.box_art_url = game.box_art_url.replace("{width}", "300").replace("{height}", "400")
        

    for stream in recent_streams:
        stream.streamer_id = stream.id
        stream.user_name = stream.user_name
        stream.user_id = stream.user_id
        stream.title = stream.title
        stream.game_id = stream.game_id
        stream.game_name = stream.game_name
        stream.viewer_count = stream.viewer_count
        stream.started_at = stream.started_at
        stream.profile_image_url = stream.thumbnail_url.replace("{width}", "300").replace("{height}", "400")

    # Reverses the List as 20th most recent would show first otherwise
    games = list(recent_games)[::-1]
    streams = list(recent_streams)[::-1]



    # Contact Form Information
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

                messages.success(request, "Email sent successfully!")
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
    user = request.user
    game = get_object_or_404(Game, game_id = game_id)
    game.box_art_url = game.box_art_url.replace("{width}", "300").replace("{height}", "400")
    if user.is_authenticated:
        is_favorited = FavoriteGame.objects.filter(user=user, favorite_games=game).exists()
    else:
        is_favorited = False

    
    # Fetches current streamers of Game
    url = f"https://api.twitch.tv/helix/streams?game_id={game_id}"
    response = requests.get(url, headers=HEADERS)
    streams = []

    # Fetches Game's past 30 day history from twitchtracker.com
    tturl = f"https://twitchtracker.com/api/games/summary/{game_id}"
    ttresponse = requests.get(tturl)


    # Game Data from Twitch.tv
    if response.status_code == 200:
        data = response.json().get("data", [])
        
        for stream in data:
            streams.append({
                "user_name": stream["user_name"],
                "user_login": stream["user_login"],
                "title": stream["title"],
                "viewer_count": stream["viewer_count"],
                "started_at": stream["started_at"],
                "url": f"https://www.twitch.tv/{stream["user_login"]}",
                "thumbnail_url": stream["thumbnail_url"].replace("{width}", "300").replace("{height}", "400")
            })


    # Game Data from TwitchTracker.com
    if ttresponse.status_code == 200:
        pdata = ttresponse.json()
        # pdata will hold 'avg_viewers', 'avg_channels', 'rank', and 'hours_watched'
        key_change = {
            "avg_viewers": "Average # of Viewers",
            "avg_channels": "Average # of Channels Streaming",
            "rank": "Average Rank",
            "hours_watched": "Average # of Hours Watched Across All Streamers",
        }
        updated_pdata = {key_change.get(k, k): v for k, v in pdata.items()}
        


    return render(request, "pages/game_detail.html", {"game": game, "streams": streams, "is_favorited":is_favorited, "updated_pdata": updated_pdata})


def streamer_detail(request, user_id):
    user = request.user
    streamer = get_object_or_404(StreamData, user_id = user_id)
    user_login = streamer.user_login
    streamer.thumbnail_url = streamer.thumbnail_url.replace("{width}", "300").replace("{height}", "400")
    if user.is_authenticated:
        is_favorited = FavoriteStreamer.objects.filter(user=user, favorite_streamers=streamer).exists()
    else:
        is_favorited = False

    # Fetches current streaming stats
    url =f"https://api.twitch.tv/helix/streams?user_id={user_id}"
    response = requests.get(url, headers=HEADERS)

    # Fetching past videos
    videos_url = f"https://api.twitch.tv/helix/videos?user_id={user_id}"
    videos_response = requests.get(videos_url, headers=HEADERS)
    videos_data = videos_response.json().get("data", [])

    # Fetches Streamer's past 30 day history from twitchtracker.com
    tturl = f"https://twitchtracker.com/api/channels/summary/{user_login}"
    ttresponse = requests.get(tturl)
    

    for video in videos_data:
        if "thumbnail_url" in video:
            video["thumbnail_url"] = video["thumbnail_url"].replace("%{width}", "300").replace("%{height}", "400")


    if response.status_code == 200:
        if ttresponse.status_code == 200:
            pdata = ttresponse.json()
            # pdata will hold 'rank', 'minutes_streamed', 'avg_viewers', 'max_viewers', 'hours_watched', 'followers', and 'followers_total'
            key_change = {
            "rank": "Average Rank",
            "minutes_streamed": "Total # of Minutes Streamed",
            "avg_viewers": "Average # of Viewers",
            "max_viewers": "Highest # of Viewers Total",
            "hours_watched": "Total # of Hours Watched",
            "followers": "# of New Followers",
            "followers_total": "Total # of Followers",
            }
        else:
            pdata = {}

    updated_pdata = {key_change.get(k, k): v for k, v in pdata.items()}

    return render(request, "pages/streamer_detail.html", {"streamer": streamer, "videos_data": videos_data, "is_favorited": is_favorited, "updated_pdata": updated_pdata})


# Contact View
def contact_view(request):
    
    return render(request, 'pages/contact.html', {})



# Registration View
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})

# Login/Registration View
def login_register(request):
    if request.method == "POST":
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user = authenticate(
                username=login_form.cleaned_data["username"],
                password=login_form.cleaned_data["password"]
            )
            if user is not None:
                login(request, user)
                return redirect("home")
    else:
        login_form = AuthenticationForm()

    register_form = CustomUserCreationForm()
    
    return render(request, "registration/login.html", {"login_form": login_form, "register_form": register_form})


# Handling favorite
@login_required
def toggle_favorite(request):
    if request.method == "POST":
        user = request.user
        data = json.loads(request.body)

        # Make sure to check whether game or streamer
        game_id = data.get("game_id")
        streamer_id = data.get("streamer_id")

        if game_id:
            game = get_object_or_404(Game, id=game_id)
            existing_favorite = FavoriteGame.objects.filter(user=user, favorite_games=game).first()
            if existing_favorite:
                # If already favorited, removes it
                existing_favorite.delete()
                return JsonResponse({"message": "Removed from favorites", "status": "removed"})
            else:
                # If NOT favorited, add it to favorites
                FavoriteGame.objects.create(user=user, favorite_games=game)
                return JsonResponse({"message": "Added to favorites","status": "added"})


        if streamer_id:
            streamer = get_object_or_404(StreamData, id=streamer_id)
            existing_favorite = FavoriteStreamer.objects.filter(user=user, favorite_streamers=streamer).first()
            if existing_favorite:
                # If already favorited, removes it
                existing_favorite.delete()
                return JsonResponse({"message": "Removed from favorites", "status": "removed"})
            else:
                # If NOT favorited, add it to favorites
                FavoriteStreamer.objects.create(user=user, favorite_streamers=streamer)
                return JsonResponse({"message": "Added to favorites","status": "added"})
    

# User Profile View
def profile_view(request):
    user = request.user
    favorite_games = Game.objects.filter(favorite_games__user=user).all()
    favorite_streamers = StreamData.objects.filter(favorite_streamers__user=user).all()

    for game in favorite_games:
        game.box_art_url = game.box_art_url.replace("{width}", "300").replace("{height}", "400")

    for streamer in favorite_streamers:
        streamer.profile_image_url = streamer.thumbnail_url.replace("{width}", "300").replace("{height}", "400")



    return render(request, "pages/profile.html", {"favorite_games": favorite_games, "favorite_streamers": favorite_streamers})