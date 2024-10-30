from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db.models import UniqueConstraint
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    poster = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="poster")
    time = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=1000, default="")
    likes = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    reply_to = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name="reply")
    is_reply = models.BooleanField(default=False)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["poster", "time", "content"], name="unique_post")
        ]


class Followship(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed")

    class Meta:
        constraints = [
            UniqueConstraint(fields=["follower", "followed"], name="unique_followship")
        ]


class Likeship(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_post", default=1)
    liker = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="liker")

    class Meta:
        constraints = [
            UniqueConstraint(fields=["post", "liker"], name="unique_likeship")
        ]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="commented_post", default=1)
    commenter = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="commenter")
    time = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=400)
    likes = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    reply_to = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name="reply_comment")
    location = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    is_reply = models.BooleanField(default=False)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["commenter", "time", "content"], name="unique_comment")
        ]


class Likeship_comment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="liked_comment", default=1)
    liker = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="liker_comment")

    class Meta:
        constraints = [
            UniqueConstraint(fields=["comment", "liker"], name="unique_likeship_comment")
        ]


class Archive(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="archive")
    time = models.DateTimeField(auto_now_add=True)
    private = models.BooleanField(default=False)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["name", "owner"], name="unique_archive")
        ]


class Archived(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="archived_post", default=1)
    archiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="archiver")
    archive = models.ManyToManyField(Archive, related_name="archived_location", null=True, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["post", "archiver"], name="unique_archived")
        ]


class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    alias = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    self_intro = models.CharField(max_length=1000, null=True, blank=True)
