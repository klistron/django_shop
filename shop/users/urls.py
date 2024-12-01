from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    MeganoLoginView,
    ChangePasswordView,
    MeganoRegisterView,
    ProfileView,
    AvatarAPIView,
)


app_name = "users"

urlpatterns = [
    path("api/sign-in", MeganoLoginView.as_view(), name="post_sign_in"),
    path("api/sign-out", LogoutView.as_view(), name="post_sign_out"),
    path("api/sign-up", MeganoRegisterView.as_view(), name="post_sign_up"),
    path("api/profile", ProfileView.as_view(), name="profile"),
    path("api/profile/avatar", AvatarAPIView.as_view(), name="avatar"),
    path("api/profile/password", ChangePasswordView.as_view(), name="password"),
]
