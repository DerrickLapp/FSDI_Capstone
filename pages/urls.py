from django.urls import path
from .views import home_view, game_detail


urlpatterns = [
    path("", home_view, name="root"),
    path("home/", home_view, name="home"),
    path("pages/<int:game_id>/", game_detail, name="game_detail"),
]
