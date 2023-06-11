from django.urls import path
from accounts import views
from django.contrib.auth.views import LogoutView

app_name = "accounts"

urlpatterns = [
    path("sign-in/", views.UserLoginAPIView.as_view(), name="post_sign_in"),
    path("sign-out/", LogoutView.as_view(), name="post_sign_out"),
    path("sign-up/", views.UserRegisterAPIView.as_view(), name="post_sign_up"),
    path("profile/", views.ProfileUpdateAPIView.as_view(), name="post_profile"),
    path(
        "profile/password/",
        views.ChangePasswordApiView.as_view(),
        name="post_profile_password",
    ),
    path(
        "profile/avatar/",
        views.ChangeAvatarAPIView.as_view(),
        name="post_profile_avatar",
    ),
]
