from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password, ValidationError
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
import json
from .models import Profile


class UserLoginAPIView(APIView):
    def post(self, request: Request):
        body = json.loads(request.body)
        username = body.get("username")
        password = body.get("password")
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response(status=200)
        return Response(status=400)


class UserRegisterAPIView(APIView):
    def post(self, request: Request):
        body = json.loads(request.body)
        username = body.get("username")
        password = body.get("password")
        name = body.get("name")
        try:
            validate_password(password)
        except ValidationError:
            return Response(status=400)
        user = User.objects.create_user(
            username=username,
            password=password,
        )
        Profile.objects.create(user=user, full_name=name)
        login(request, user)
        return Response(status=200)


class ProfileUpdateAPIView(APIView):
    def post(self, request: Request):
        user = request.user
        if user.is_authenticated:
            data = request.data
            user.profile.full_name = data.get("fullName")
            user.email = data.get("email")
            user.profile.phone_number = data.get("phone")
            user.profile.save()
            user.save()
            return Response(status=200, data=data)
        return Response(status=400)

    def get(self, request: Request):
        if request.user.is_authenticated:
            user = request.user
            data = {
                "fullName": user.profile.full_name,
                "email": user.email,
                "phone": user.profile.phone_number,
                "avatar": {
                    "src": user.profile.avatar.url,
                    "alt": user.profile.avatar.name,
                },
            }
            return Response(data=data, status=200)
        return Response(status=400)


class ChangePasswordApiView(APIView):
    def post(self, request: Request):
        user: User = request.user
        if user.is_authenticated:
            data = request.data
            password = data.get("passwordCurrent")
            new_password1 = data.get("password")
            new_password2 = data.get("passwordReply")
            if new_password2 == new_password1 and user.check_password(password):
                try:
                    validate_password(new_password1)
                    user.set_password(new_password1)
                    user.save()
                    login(request, user)
                    return Response(status=200)
                except ValidationError:
                    print("Non valid")
        return Response(status=400)


class ChangeAvatarAPIView(APIView):
    def post(self, request: Request):
        user: User = request.user
        if user.is_authenticated:
            avatar = request.data.get("avatar")
            if avatar.size < 2 * 1024 * 1024:
                user.profile.avatar = avatar
                user.profile.save()
                data = {"src": user.profile.avatar.url, "alt": user.profile.avatar.name}
                return Response(status=200, data=data)
            else:
                print('avatar bigger then 2 mb')
        return Response(status=400)
