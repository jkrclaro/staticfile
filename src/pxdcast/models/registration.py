from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver


CITIES = (
    ('dublin', 'Dublin'),
)


class ProfileManager(models.Manager):
    pass


class User(AbstractUser):
    pass


class Profile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    objects = ProfileManager()

    class Meta:
        db_table = 'profiles'

    def __str__(self):
        return self.user.username