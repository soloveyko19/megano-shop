from django.db import models
from django.contrib.auth.models import User


def upload_avatar_path(instance: "Profile", filename: str) -> str:
    return "users/user_{pk}/avatars/{filename}".format(
        pk=instance.user.pk, filename=filename
    )


class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    avatar = models.ImageField(null=True, upload_to=upload_avatar_path)

    def __str__(self):
        return "profile {user}".format(user=self.user.username)

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"
