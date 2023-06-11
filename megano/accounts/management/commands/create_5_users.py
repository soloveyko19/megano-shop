from django.core.management import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(1, 6):
            user = User.objects.create_user(username=f"user_{i}", password="12345678")
            Profile.objects.create(
                user=user,
            )
