import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from .serializers import (
    LoginSerializer,
    UserRegistrationSerializer,
    ProfileSerializer,
    AvatarSerializer,
)
from .models import Profile, Avatar


class MeganoLoginView(APIView):
    def post(self, request):
        if isinstance(request.body, bytes):
            request_body = request.body.decode("utf-8")
        else:
            request_body = request.body

        data = json.loads(request_body)
        serializer = LoginSerializer(data=data)

        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return Response({"message": "Успешный вход"}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Неверный логин или пароль"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeganoRegisterView(APIView):
    def post(self, request):
        if isinstance(request.body, bytes):
            request_body = request.body.decode("utf-8")
        else:
            request_body = request.body

        data = json.loads(request_body)
        serializer = UserRegistrationSerializer(data=data)

        if serializer.is_valid():
            user = serializer.save()
            user.first_name = data["name"]
            user.save()
            login(request, user)
            return Response(
                {"message": "Пользователь успешно зарегистрирован", "user_id": user.id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        print("ready")
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AvatarAPIView(APIView):
    def post(self, request):
        profile = get_object_or_404(Profile, user=request.user)

        # Проверяем, есть ли файл аватара в запросе
        if "avatar" not in request.FILES:
            return Response(
                {"error": "No avatar file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        avatar_file = request.FILES["avatar"]

        avatar, created = Avatar.objects.get_or_create(profile=profile)
        avatar.src = avatar_file
        avatar.alt = request.data.get("alt", "")  # Если предоставлено описание
        avatar.save()

        serializer = AvatarSerializer(avatar)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current_password = request.data.get('currentPassword')
        new_password = request.data.get('newPassword')

        if not current_password or not new_password:
            return Response(
                {"error": "Both current password and new password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=request.user.username, password=current_password)
        if user is None:
            return Response(
                {"error": "Current password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {"message": "Password successfully changed."},
            status=status.HTTP_200_OK
        )
