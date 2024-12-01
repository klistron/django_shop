from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    fullName = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Полное имя"
    )
    email = models.EmailField(max_length=50, verbose_name="Электронная почта")
    phone = models.CharField(
        max_length=12, blank=True, null=True, verbose_name="Телефон"
    )

    class Meta:
        verbose_name = "Профиль пользователя"

    def __str__(self) -> str:
        return self.fullName


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


def avatar_directory_path(instance: "Avatar", filename: str) -> str:
    """Путь к изображению товара"""
    return "avatars/profile_{pk}/avatar/{filename}".format(
        pk=instance.profile.pk,
        filename=filename,
    )


class Avatar(models.Model):
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name="avatar"
    )
    src = models.ImageField(upload_to=avatar_directory_path, verbose_name="Ссылка")
    alt = models.CharField(
        max_length=100, null=False, blank=True, verbose_name="Описание"
    )

    class Meta:
        verbose_name = "Аватар пользователя"

    def __str__(self) -> str:
        return self.alt
