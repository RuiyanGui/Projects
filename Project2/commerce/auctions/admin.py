from django.contrib import admin
from .models import Listing, Comment, Bidding, Watchlist, User

# Register your models here.
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Bidding)
admin.site.register(Watchlist)
admin.site.register(User)
