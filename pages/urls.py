from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home_view, game_detail, streamer_detail, register, login_register, toggle_favorite


urlpatterns = [
    path("", home_view, name="root"),
    path("home/", home_view, name="home"),
    path("pages/game/<int:game_id>/", game_detail, name="game_detail"),
    path("pages/streamer/<int:user_id>/", streamer_detail, name="streamer_detail"),
    path("login/", login_register, name="login"),
    path("register/", register, name="register"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("toggle_favorite/", toggle_favorite, name="toggle_favorite"),
]
