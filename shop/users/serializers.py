from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Avatar, Profile


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            return attrs
        else:
            raise serializers.ValidationError(
                "Необходимо указать имя пользователя и пароль."
            )


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data):
        user = User(
            username=validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()
        buyers_group = Group.objects.get(name="Покупатели")
        user.groups.add(buyers_group)  # Добавляем пользователя в группу "Покупатели"
        return user


class AvatarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ["src", "alt"]


class ProfileSerializer(serializers.ModelSerializer):
    avatar = AvatarImageSerializer(required=False, allow_null=True)

    class Meta:
        model = Profile
        fields = [
            "fullName",
            "email",
            "phone",
            "avatar",
        ]

    def update(self, instance, validated_data):
        avatar_data = validated_data.pop("avatar", None)
        if avatar_data:
            Avatar.objects.update_or_create(profile=instance, defaults=avatar_data)

        return super().update(instance, validated_data)


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ['src', 'alt']

    def update(self, instance, validated_data):
        instance.src = validated_data.get('src', instance.src)
        instance.alt = validated_data.get('alt', instance.alt)
        instance.save()
        return instance