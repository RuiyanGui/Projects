from django.contrib import admin
from .models import Followship, Post, Likeship

# Register your models here.
admin.site.register(Followship)
admin.site.register(Post)
admin.site.register(Likeship)
