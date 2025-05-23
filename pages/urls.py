from django.urls import path
from .views import home_view, game_detail, streamer_detail


urlpatterns = [
    path("", home_view, name="root"),
    path("home/", home_view, name="home"),
    path("pages/game/<int:game_id>/", game_detail, name="game_detail"),
    path("pages/streamer/<int:user_id>/", streamer_detail, name="streamer_detail"),
]
