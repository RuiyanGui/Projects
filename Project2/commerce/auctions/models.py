from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings


# SuperUser's username: 123, password:123456
class User(AbstractUser):
    pass

class Listing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    activity = models.BooleanField(default=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=400, default="something")
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.00)])
    category = models.CharField(max_length=20, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)

class Bidding(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidding = models.DecimalField(max_digits=8, decimal_places=2)

class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
