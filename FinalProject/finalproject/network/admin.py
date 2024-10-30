from django.contrib import admin
from .models import User, Followship, Post, Likeship, Likeship_comment, Comment, Archive, Archived, Profile

# Register your models here.
admin.site.register(Followship)
admin.site.register(Post)
admin.site.register(Likeship)
admin.site.register(Likeship_comment)
admin.site.register(Comment)
admin.site.register(Archived)
admin.site.register(Archive)
admin.site.register(Profile)
admin.site.register(User)
