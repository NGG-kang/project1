from django.contrib.auth.models import AbstractUser
from django.db import models

from django_auto_one_to_one import AutoOneToOneModel


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    following_set = models.ManyToManyField("self", blank=True)
    follower_set = models.ManyToManyField("self", blank=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254, blank=True)


def user_profile_path(instance, filename):
    return 'nboard/profile/user_{}/{}'.format(instance.user, filename)


class Profile(AutoOneToOneModel(User)):
    user_photo = models.ImageField(blank=True, upload_to=user_profile_path)
    status_message = models.CharField(blank=True, max_length=300)
