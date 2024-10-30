from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    poster = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="poster")
    time = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=400)
    likes = models.IntegerField(default=0, validators=[MinValueValidator(0)])


class Followship(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed")


class Likeship(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_post", default=1)
    liker = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="liker")
