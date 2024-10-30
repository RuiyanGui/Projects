
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:user_id>", views.display_profile, name="profile"),
    path("follow", views.follow, name="follow"),
    path("following", views.display_following, name="following"),
    path("comment/<int:post_id>", views.comment, name="comment"),
    path("archive", views.archive, name="archive"),
    path("archive_view/<int:archive_id>", views.archive_view, name="archive_view"),
    path("edit_profile", views.edit_profile, name="edit_profile"),

    path("edit", views.edit, name="edit"),
    path("like", views.like, name="like"),
    path("delete", views.delete, name="delete"),
    path("reply", views.reply, name="reply")
]
