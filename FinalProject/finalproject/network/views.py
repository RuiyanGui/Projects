from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.forms import ModelForm
from django.core.exceptions import EmptyResultSet, ObjectDoesNotExist
from django.core.paginator import Paginator
import json


from .models import User, Post, Followship, Likeship, Likeship_comment, Comment, Archived, Archive, Profile


# Define forms.
class PostForm(ModelForm):
    poster = ""
    content = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={
        "autofocus": True,
        "rows": 5,
        "cols": 80,
        "class": "form-control bg-dark",
        "style": "color: white"
        }))
    time = ""

    class Meta:
        model = Post
        fields = ["content"]


class CommentForm(ModelForm):
    post = ""
    commenter = ""
    content = forms.CharField(max_length=400, widget=forms.Textarea(attrs={
        "autofocus": True,
        "rows": 5,
        "cols": 80,
        "class": "form-control bg-dark",
        "style": "color: white"
        }))
    time = ""

    class Meta:
        model = Comment
        fields = ["content"]


class ArchiveForm(ModelForm):
    name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        "class": "form-control bg-dark",
        "style": "color: white; width: 40vw; max-width: 200px"
    }))
    owner = ""
    time = ""
    private = forms.BooleanField

    class Meta:
        model = Archive
        fields = ["name", "private"]


class ProfileForm(ModelForm):
    owner = ""
    alias = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        "autofocus": "true",
        "class": "form-control bg-dark",
        "style": "color: white"
        }))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={
        "class": "form-control bg-dark",
        "style": "color: white"
        }))
    self_intro = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={
        "class": "form-control bg-dark",
        "style": "color: white"
        }))

    class Meta:
        model = Profile
        fields = ["alias", "date_of_birth", "self_intro"]


# Paginate items.
def paginate(items, request, module):
    if module == "post":
        paginator = Paginator(items, 10)
        page_number = request.GET.get('page')
        items_per_page = paginator.get_page(page_number)

    elif module == "comment":
        paginator = Paginator(items, 10)
        page_number = request.GET.get('comment_page')
        items_per_page = paginator.get_page(page_number)

    elif module == "liker":
        paginator = Paginator(items, 20)
        page_number = request.GET.get('liker_page')
        items_per_page = paginator.get_page(page_number)

    elif module == "archive":
        paginator = Paginator(items, 5)
        page_number = request.GET.get('archive_page')
        items_per_page = paginator.get_page(page_number)

    elif module == "follower":
        paginator = Paginator(items, 20)
        page_number = request.GET.get('follower_page')
        items_per_page = paginator.get_page(page_number)

    elif module == "followed":
        paginator = Paginator(items, 20)
        page_number = request.GET.get('followed_page')
        items_per_page = paginator.get_page(page_number)

    return items_per_page


def index(request):

    # Get index page.
    if request.method == "GET":
        try:
            posts = Post.objects.all().order_by("-time")
        except EmptyResultSet:
            posts = None

        # Append archive locations and number of comments to each post.
        for post in posts:
            archived = Archived.objects.filter(post=post, archiver=request.user.id).first()
            try:
                archived_locations = archived.archive.filter(owner=request.user.id)
            except AttributeError:
                archived_locations = []
            comments_count = Comment.objects.filter(post=post.id).count()
            post.comments_count = comments_count
            post.archived_locations = archived_locations

        # Get liked posts.
        liked_posts = []
        likes = Likeship.objects.filter(liker=request.user.id)
        for like in likes:
            print(like.post)
            liked_posts.append(like.post)

        print(liked_posts)

        # Get archives.
        archives = Archive.objects.filter(owner=request.user.id).order_by("-id")

        # Render page.
        posts_per_page = paginate(posts, request, module="post")

        return render(request, "network/index.html", {
            "form": PostForm,
            "posts": posts,
            "posts_per_page": posts_per_page,
            "liked_posts": liked_posts,
            "archives": archives
        })

    # Send new post.
    elif request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.poster = request.user
            data.save()
        return HttpResponseRedirect(reverse("index"))


def display_profile(request, user_id):

    # Try to fetch profile.
    try:
        profile_owner = User.objects.get(pk=user_id)

    except ObjectDoesNotExist:
        messages.warning(request, "The requested profile does not exist.")
        return HttpResponseRedirect(reverse("index"))

    # Get relevant info.
    try:
        posts = Post.objects.filter(poster=profile_owner).order_by("-id")
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
        if follower.follower.id == request.user.id:
            following_status = True

    # Get liked posts.
    liked_posts = []
    likes = Likeship.objects.filter(liker=request.user.id)
    for like in likes:
        print(like.post)
        liked_posts.append(like.post)

    print(liked_posts)

    # Append archive locations and number of comments to each post.
    for post in posts:
        archived = Archived.objects.filter(post=post, archiver=request.user.id).first()
        try:
            archived_locations = archived.archive.filter(owner=request.user.id)
        except AttributeError:
            archived_locations = []
        comments_count = Comment.objects.filter(post=post.id).count()
        post.comments_count = comments_count
        post.archived_locations = archived_locations

    archives = Archive.objects.filter(owner=profile_owner).order_by("-id")
    myarchives = Archive.objects.filter(owner=request.user.id).order_by("-id")

    # Render page.
    posts_per_page = paginate(posts, request, module="post")
    archives_per_page = paginate(archives, request, module="archive")
    followers_per_page = paginate(followers, request, module="follower")
    followeds_per_page = paginate(followeds, request, module="followed")
    followeds_count = followeds.count()
    followers_count = followers.count()

    return render(request, "network/profile.html", {
        "posts": posts,
        "posts_per_page": posts_per_page,
        "profile_owner": profile_owner,
        "login_user": request.user,
        "followers_per_page": followers_per_page,
        "followeds_per_page": followeds_per_page,
        "followers_count": followers_count,
        "followeds_count": followeds_count,
        "following_status": following_status,
        "archive_form": ArchiveForm,
        "archives_per_page": archives_per_page,
        "archives": myarchives,
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

    # Check if the user is deleted before they are followed.
    try:
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

    except ObjectDoesNotExist:
        messages.warning(request, "Profile is deleted.")
        return HttpResponseRedirect(reverse("index"))

    return HttpResponseRedirect(reverse("profile", args=[followed_user.id]))


@login_required
def display_following(request):

    # Get relevant info.
    login_user = User.objects.get(pk=request.user.id)
    followeds = Followship.objects.filter(follower=login_user)

    # Get posts and append to each post its archive locations and number of comments.
    posts = []
    for followed in followeds:
        followed_posts = Post.objects.filter(poster=followed.followed)
        for followed_post in followed_posts:
            archived = Archived.objects.filter(post=followed_post, archiver=request.user.id).first()
            try:
                archived_locations = archived.archive.filter(owner=request.user.id)
            except AttributeError:
                archived_locations = []
            comments_count = Comment.objects.filter(post=followed_post.id).count()
            followed_post.comments_count = comments_count
            followed_post.archived_locations = archived_locations
            posts.append(followed_post)

    posts.sort(reverse=True, key=lambda x: x.time)
    posts_per_page = paginate(posts, request, module="post")

    # Get liked posts.
    liked_posts = []
    likes = Likeship.objects.filter(liker=request.user.id)
    for like in likes:
        liked_posts.append(like.post)

    # Get archives.
    archives = Archive.objects.filter(owner=request.user.id).order_by("-id")

    # Render page.
    return render(request, "network/following.html", {
        "posts_per_page": posts_per_page,
        "liked_posts": liked_posts,
        "archives": archives
    })


@login_required
def edit(request):

    # Send prefill content to frontend.
    if request.method == "POST":
        data = json.loads(request.body)
        id = data.get("id")
        module = data.get("module")

        if module == "post":
            post = Post.objects.get(pk=id)
            content = post.content

        else:
            comment = Comment.objects.get(pk=id)
            content = comment.content

        return JsonResponse(content, safe=False)

    # Save new content.
    elif request.method == "PUT":
        data = json.loads(request.body)
        new_content = data.get("new_content")
        id = data.get("id")
        module = data.get("module")

        if module == "post":
            post = Post.objects.get(pk=id)
            post.content = new_content

            print(f"{post.content} is said in this {post.id} post by {post.poster}")

            post.save()

        else:
            comment = Comment.objects.get(pk=id)
            comment.content = new_content
            comment.save()

        return HttpResponse(status=204)

    # Deny other requests.
    else:
        return JsonResponse({
            "error": "POST or PUT request required."
        }, status=400)


@login_required
def like(request):

    # Save new like backend.
    if request.method == "PUT":
        data = json.loads(request.body)
        id = data.get("id")
        module = data.get("module")

        if module == "comment":

            # Check if the post is deleted before it is liked.
            try:
                comment = Comment.objects.get(pk=id)
                comment.likes += 1
                comment.save()
                new_like = Likeship_comment(liker=request.user, comment=comment)
                new_like.save()
                like_count = comment.likes

            except ObjectDoesNotExist:
                like_count = None

        else:

            # Check if the comment is deleted before it is liked.
            try:
                post = Post.objects.get(pk=id)
                post.likes += 1
                post.save()
                new_like = Likeship(liker=request.user, post=post)
                new_like.save()
                like_count = post.likes

            except ObjectDoesNotExist:
                like_count = None

        # Send it back to frontend.
        return JsonResponse(like_count, safe=False)

    # Delete like backend.
    elif request.method == "DELETE":
        data = json.loads(request.body)
        id = data.get("id")
        module = data.get("module")

        if module == "post":

            # Check if the post is deleted before it is unliked.
            try:
                post = Post.objects.get(pk=id)
                post.likes -= 1
                post.save()
                like = Likeship.objects.filter(liker=request.user.id, post=post)
                like.delete()
                like_count = post.likes

            except ObjectDoesNotExist:
                like_count = None

        else:

            # Check if the comment is deleted before it is unliked.
            try:
                comment = Comment.objects.get(pk=id)
                comment.likes -= 1
                comment.save()
                like = Likeship_comment.objects.filter(liker=request.user.id, comment=comment)
                like.delete()
                like_count = comment.likes

            except ObjectDoesNotExist:
                like_count = None

        return JsonResponse(like_count, safe=False)

    # Deny other requests.
    else:
        return JsonResponse({
            "error": "POST or PUT request required."
        }, status=400)


def comment(request, post_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.commenter = request.user

            # Try to get the post.
            try:
                post = Post.objects.get(pk=post_id)
                data.post = post
                location = Comment.objects.filter(post=post).count() + 1
                data.location = location
                data.save()

            except ObjectDoesNotExist:
                messages.warning(request, "The Post is deleted.")
                return HttpResponseRedirect(reverse("index"))

        return HttpResponseRedirect(reverse("comment", args=[post_id]))
    else:

        # Try to get the post.
        try:
            post = Post.objects.get(pk=post_id)

            # Get comments.
            comments = Comment.objects.filter(post=post).order_by("-id")
            post.comments_count = comments.count()
            comments_per_page = paginate(comments, request, module="comment")
            liked_comments = []
            likes_comments = Likeship_comment.objects.filter(liker=request.user.id)

            # Get likers.
            likers_of_post = Likeship.objects.filter(post=post_id).order_by("-id")
            likers_per_page = paginate(likers_of_post, request, module="liker")
            for like_comment in likes_comments:
                liked_comments.append(like_comment.comment)

            # Get liked posts.
            liked_posts = []
            likes = Likeship.objects.filter(liker=request.user.id)
            for like in likes:
                liked_posts.append(like.post)

            # Get archives and archive locations.
            archives = Archive.objects.filter(owner=request.user.id).order_by("-id")
            archived = Archived.objects.filter(post=post, archiver=request.user.id).first()
            try:
                archived_locations = archived.archive.filter(owner=request.user.id)
            except AttributeError:
                archived_locations = []
            post.archived_locations = archived_locations

            # Get replies.
            replies = Post.objects.filter(reply_to=post).order_by("-id")
            replies_per_page = paginate(replies, request, module="post")

            # Render page.
            return render(request, "network/post.html", {
                "comments_per_page": comments_per_page,
                "liked_comments": liked_comments,
                "liked_posts": liked_posts,
                "post": post,
                "comment_form": CommentForm,
                "likers_per_page": likers_per_page,
                "replies_per_page": replies_per_page,
                "archives": archives
            })

        except ObjectDoesNotExist:
            messages.warning(request, "The requested Post is deleted.")
            return HttpResponseRedirect(reverse('index'))


@login_required
def delete(request):

    # Only DELETE REQUEST is allowed.
    if request.method == "DELETE":
        data = json.loads(request.body)
        module = data.get("module")
        id = data.get("id")

        if module == "post":
            post = Post.objects.get(pk=id)
            if post.poster.id == request.user.id:
                post.delete()

        elif module == "user":
            user = User.objects.get(pk=id)
            if user.id == request.user.id:
                user.delete()

        elif module == "comment":
            comment = Comment.objects.get(pk=id)
            if comment.commenter.id == request.user.id:
                comment.delete()

        else:
            archive = Archive.objects.get(pk=id)
            if archive.owner.id == request.user.id:
                archive.delete()

        return HttpResponse(status=303)

    else:
        return JsonResponse({
            "error": "DELETE request required."
        }, status=400)


@login_required
def reply(request):

    # Only POST REQUEST is allowed.
    if request.method == "POST":

        # Get data.
        data = json.loads(request.body)
        id = data.get("id")
        module = data.get("module")
        content = data.get("content")

        # Reply to the comment.
        if module == "comment":
            post_id = data.get("post_id")

            # Check if the comment or the post is deleted.
            try:
                comment = Comment.objects.get(pk=id)
                post = Post.objects.get(pk=post_id)
                location = Comment.objects.filter(post=post).count() + 1
                reply_comment = Comment(commenter=request.user, content=content, reply_to=comment, post=post, location=location, is_reply=True)
                reply_comment.save()

            except ObjectDoesNotExist:
                messages.warning(request, "Comment is deleted.")
                return HttpResponseRedirect(reverse("comment", args=[post_id]))

            return HttpResponse(status=304)

        # Reply to the post.
        else:

            # Check if the post is deleted.
            try:
                post = Post.objects.get(pk=id)
                reply_post = Post(poster=request.user, content=content, reply_to=post, is_reply=True)
                reply_post.save()

            except ObjectDoesNotExist:
                messages.warning(request, "Post is deleted.")
                return HttpResponseRedirect(reverse("index"))

            return HttpResponse(status=304)
    else:
        JsonResponse({
            "error": "POST request required."
        }, status=400)


@login_required
def archive(request):

    # Archive the post.
    if request.method == "PUT":
        data = json.loads(request.body)
        id = data.get("id")
        archives = data.get("archives")

        # Check if the post is deleted.
        try:
            post = Post.objects.get(pk=id)

            # Check if the item is first archived or already archived.
            try:
                archived = Archived.objects.get(post=post)

            except ObjectDoesNotExist:
                archived = Archived(archiver=request.user, post=post)

            # Clear all previous archive locations the archived post has.
            archived.save()
            archived.archive.clear()

            # Add new archive locations to the archived post.
            for archive in archives:
                archived_location = Archive.objects.get(pk=archive)
                archived.archive.add(archived_location)

        except ObjectDoesNotExist:
            archived = None

        return HttpResponse(status=304)

    # Create or edit archive.
    elif request.method == "POST":
        form = ArchiveForm(request.POST)

        if form.is_valid():
            data = form.save(commit=False)

            # Edit archive.
            try:

                # Validate name before save.
                try:
                    id = request.POST["id"]
                    archive = Archive.objects.get(pk=id)
                    archive.name = data.name
                    archive.private = data.private
                    archive.save()
                except IntegrityError:
                    messages.warning(request, "you already have an archive of the same name!")
                return HttpResponseRedirect(reverse('archive_view', args=[id]))

            # Create archive.
            except KeyError:
                try:
                    data.owner = request.user
                    data.save()

                # Validate name before save.
                except IntegrityError:
                    messages.warning(request, "you already have an archive of the same name!")

        return HttpResponseRedirect(reverse('profile', args=[request.user.id]))


@login_required
def archive_view(request, archive_id):

    # Check if the archive still exists.
    try:
        archive = Archive.objects.get(pk=archive_id)

    except ObjectDoesNotExist:
        return JsonResponse({
            "error": "The Archive no longer exists."
        })

    archives = Archive.objects.filter(owner=request.user.id).order_by("-id")
    archiveds = Archived.objects.filter(archive=archive).order_by("-id")

    # Add all archive locations and comment number to each post.
    posts = []
    for archived in archiveds:
        archived.post.comments_count = Comment.objects.filter(post=archived.post.id).count()
        try:
            archived_locations = archived.archive.filter(owner=request.user.id)
        except EmptyResultSet:
            archived_locations = []
        archived.post.archived_locations = archived_locations
        posts.append(archived.post)

    # Render page.
    posts_per_page = paginate(posts, request, module="post")

    form = ArchiveForm(initial={
        "name": archive.name,
        "private": archive.private
    })

    return render(request, "network/archive.html", {
        "posts_per_page": posts_per_page,
        "archive": archive,
        "form": form,
        "archives": archives
    })


@login_required
def edit_profile(request):

    # View edit page.
    if request.method == "GET":

        # Edit profile view.
        try:
            data = Profile.objects.get(pk=request.user.id)
            form = ProfileForm(initial={
                "alias": data.alias,
                "date_of_birth": data.date_of_birth,
                "self_intro": data.self_intro
            })
            print(data.self_intro)
            print(form["self_intro"])

        # Create profile view.
        except ObjectDoesNotExist:
            form = ProfileForm

        return render(request, "network/profile_edit.html", {
            "form": form
        })

    # Save the new edit.
    else:
        form = ProfileForm(request.POST)

        # Validate form.
        if form.is_valid():
            data = form.save(commit=False)

            # Check if alias is used.
            try:
                Profile.objects.get(alias=data.alias)
                messages.warning(request, "Profile with this Alias already exists.")
                return HttpResponseRedirect(reverse("edit_profile"))

            except ObjectDoesNotExist:

                # Check if profile is edited or created.
                try:
                    profile = Profile.objects.get(pk=request.user.id)
                    profile.alias = data.alias
                    profile.date_of_birth = data.date_of_birth
                    profile.self_intro = data.self_intro

                except ObjectDoesNotExist:
                    profile = Profile(pk=request.user.id, alias=data.alias, date_of_birth=data.date_of_birth, self_intro=data.self_intro)

                profile.save()

            return HttpResponseRedirect(reverse("profile", args=[request.user.id]))

        # Warning.
        else:
            print(form.errors)
            messages.warning(request, form.errors)
            return HttpResponseRedirect(reverse("edit_profile"))


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
            messages.warning(request, "Invalid username and/or password.")
            return render(request, "network/login.html", {
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
            messages.warning(request, "Passwords must match.")
            return render(request, "network/register.html", {
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.warning(request, "Username already taken.")
            return render(request, "network/register.html", {
            })
        login(request, user)
        return HttpResponseRedirect(reverse("edit_profile"))
    else:
        return render(request, "network/register.html")
