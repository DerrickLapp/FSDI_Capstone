from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home_view, game_detail, streamer_detail, register, login_register, toggle_favorite, profile_view


urlpatterns = [
    path("", home_view, name="root"),
    path("home/", home_view, name="home"),
    path("pages/game/<int:game_id>/", game_detail, name="game_detail"),
    path("pages/streamer/<int:user_id>/", streamer_detail, name="streamer_detail"),
    path("pages/profile/", profile_view, name="profile"),
    path("login/", login_register, name="login"),
    path("register/", register, name="register"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("change_password", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path("change_password_done", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("password_reset", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("toggle_favorite/", toggle_favorite, name="toggle_favorite"),
]
