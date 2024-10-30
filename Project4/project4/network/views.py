from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.forms import ModelForm
from django.core.exceptions import EmptyResultSet, ObjectDoesNotExist
from django.core.paginator import Paginator
import json


from .models import User, Post, Followship, Likeship


# Define text form.
class PostForm(ModelForm):
    poster = ""
    content = forms.CharField(max_length=400, widget=forms.Textarea(attrs={"autofocus": True}))
    time = ""

    class Meta:
        model = Post
        fields = ["content"]


# Paginate posts.
def paginate(posts, request):
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts_per_page = paginator.get_page(page_number)

    return posts_per_page


def index(request):

    # Get index page.
    if request.method == "GET":
        try:
            posts = Post.objects.all().order_by("-time")
        except EmptyResultSet:
            posts = None

        # Get liked posts.
        liked_posts = []
        try:
            likes = Likeship.objects.filter(liker=request.user)
            for like in likes:
                liked_posts.append(like.post.id)
        except TypeError:
            liked_posts = []

        # Render page.
        posts_per_page = paginate(posts, request)

        return render(request, "network/index.html", {
            "form": PostForm,
            "posts": posts,
            "posts_per_page": posts_per_page,
            "liked_posts": liked_posts
        })

    # Send new post.
    elif request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.poster = request.user
            data.save()
        return HttpResponseRedirect(reverse("index"))

    # Deny other requests.
    else:
        HttpResponse("good")


def display_profile(request, user_id):

    # Try to fetch profile.
    try:
        profile_owner = User.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        return JsonResponse({
            "error": "The profile no longer exists."
            }, status=420)

    # Get relevant info.
    try:
        posts = Post.objects.filter(poster=profile_owner).order_by("-time")
    except EmptyResultSet:
        posts = None
    try:
        followeds = Followship.objects.filter(follower=profile_owner)
    except EmptyResultSet:
        followeds = None
    try:
        followers = Followship.objects.filter(followed=profile_owner)
    except EmptyResultSet:
        followers = None

    # Check following status.
    following_status = False

    for follower in followers:
        print(f"{follower.follower.id} {request.user.id}")
        if follower.follower.id == request.user.id:
            following_status = True

    # Get liked posts.
    liked_posts = []
    try:
        likes = Likeship.objects.filter(liker=request.user)
        for like in likes:
            liked_posts.append(like.post.id)
    except TypeError:
        liked_posts = []

    # Render page.
    posts_per_page = paginate(posts, request)

    return render(request, "network/profile.html", {
        "posts": posts,
        "posts_per_page": posts_per_page,
        "profile_owner": profile_owner,
        "login_user": request.user,
        "followers": followers,
        "followeds": followeds,
        "following_status": following_status,
        "liked_posts": liked_posts
    })


@login_required
def follow(request):
    # Deny requests other than post.
    if request.method != "POST":
        return JsonResponse({
            "error": "Only accept post method."
        })

    # Get relevant info.
    followed = request.POST["followed"]
    login_user = User.objects.get(pk=request.user.id)
    followed_user = User.objects.get(username=followed)

    # Unfollow.
    if request.POST["status"] == "unfollow":
        data = Followship.objects.filter(follower=login_user, followed=followed_user)
        data.delete()

    # Follow.
    else:
        data = Followship(followed=followed_user, follower=login_user)
        data.save()

    return HttpResponseRedirect(reverse("profile", args=[followed_user.id]))


@login_required
def display_following(request):

    # Get relevant info.
    login_user = User.objects.get(pk=request.user.id)
    followeds = Followship.objects.filter(follower=login_user)

    # Get posts.
    posts = []
    for followed in followeds:
        followed_posts = Post.objects.filter(poster=followed.followed)
        print(f"{followed.followed} posts {followed_posts}")
        for followed_post in followed_posts:
            posts.append(followed_post)

    posts.sort(reverse=True, key=lambda x: x.time)
    posts_per_page = paginate(posts, request)

    # Get liked posts.
    liked_posts = []
    try:
        likes = Likeship.objects.filter(liker=request.user)
        for like in likes:
            liked_posts.append(like.post.id)
    except TypeError:
        liked_posts = []

    # Render page.
    return render(request, "network/following.html", {
        "posts_per_page": posts_per_page,
        "liked_posts": liked_posts
    })


def edit(request):

    # Send prefill content to frontend.
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data.get("post_id")
        post = Post.objects.get(pk=post_id)
        content = post.content

        return JsonResponse(content, safe=False)

    # Save new content.
    elif request.method == "PUT":
        data = json.loads(request.body)
        new_content = data.get("new_content")
        post_id = data.get("post_id")
        post = Post.objects.get(pk=post_id)
        post.content = new_content

        print(f"{post.content} is said in this {post.id} post by {post.poster}")

        post.save()

        return HttpResponse(status=204)

    # Deny other requests.
    else:
        return JsonResponse({
            "error": "POST or PUT request required."
        }, status=400)


def like(request):

    # Save new like backend.
    if request.method == "PUT":
        data = json.loads(request.body)
        post_id = data.get("post_id")
        post = Post.objects.get(pk=post_id)
        post.likes += 1
        post.save()
        new_like = Likeship(liker=request.user, post=post)
        new_like.save()
        return HttpResponse(status=204)

    # Delete like backend.
    elif request.method == "DELETE":
        data = json.loads(request.body)
        post_id = data.get("post_id")
        post = Post.objects.get(pk=post_id)
        post.likes -= 1
        post.save()
        like = Likeship.objects.filter(liker=request.user.id, post=post_id)
        like.delete()
        return HttpResponse(status=205)

    # Deny other requests.
    else:
        return JsonResponse({
            "error": "POST or PUT request required."
        }, status=400)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
