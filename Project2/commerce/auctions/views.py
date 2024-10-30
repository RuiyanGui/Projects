from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.forms import ModelForm
from django.contrib import messages
from django.core.exceptions import EmptyResultSet, ObjectDoesNotExist

from .models import User, Listing, Comment, Bidding, Watchlist


# Create ModelForm Objects.
class BiddingForm(ModelForm):
    user = ""
    bidding = forms.DecimalField(max_digits=8, decimal_places=2)
    item = ""

    class Meta:
        model = Bidding
        fields = ["bidding"]


class CommentForm(ModelForm):
    user = ""
    comment = forms.CharField(max_length=500, widget=forms.Textarea)
    item = ""

    class Meta:
        model = Comment
        fields = ["comment"]


# Render active listings to the index page.
def index(request):

    # Check if there exist active listings.
    try:
        listings = Listing.objects.filter(activity=True).order_by("-id")
    except EmptyResultSet:
        listings = None

    header = "Active Listings"
    return render(request, "auctions/index.html", {
        "listings": listings,
        "header": header
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):

    # Define ModelForm for listing objects.
    class ListingForm(ModelForm):
        user = ""
        activity = True
        title = forms.CharField(max_length=64, widget=forms.TextInput)
        description = forms.CharField(max_length=400, widget=forms.Textarea)
        starting_bid = forms.DecimalField(max_digits=8, decimal_places=2, min_value=0)
        category = forms.CharField(max_length=20, required=False)
        image_url = forms.URLField(required=False)

        class Meta:
            model = Listing
            fields = ["title", "description", "starting_bid", "category", "image_url"]

    # Check and save the submitted form.
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.category = data.category.capitalize()
            data.save()
            return HttpResponseRedirect(reverse("display", args=[data.id]))
        else:
            error_message = "Input is not valid."
            return render(request, "auctions/error.html", {
                "message": error_message
            })

    # Render the page.
    else:
        return render(request, "auctions/create.html", {
            "form": ListingForm
        })


def display_listing(request, listing_id):

    # Check if there exists such a listing.
    try:
        listing = Listing.objects.get(pk=listing_id)

        # Check if there exist comments for this listing.
        try:
            comments = Comment.objects.filter(item=listing_id).order_by("-pk")
        except EmptyResultSet:
            comments = ""

        # Check if the current listing is active.
        status = listing.activity
        if status:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "form": BiddingForm,
                "user": request.user,
                "comments": comments,
                "comment_form": CommentForm
            })

        # Show the user the listing is inactive, if it is so.
        else:
            messages.success(request, "this listing is closed!")

            # Show the winner if they win.
            try:
                highest_bid = Bidding.objects.filter(item=listing_id).last()

                if highest_bid.user == request.user:
                    messages.success(request, "You won the bid!")

            # If the listing is closed before anyone bids.
            except AttributeError:
                messages.success(request, "no one bids before the listing is closed.")

            return render(request, "auctions/listing.html", {
                "listing": listing,
                "comments": comments,
                "comment_form": CommentForm
            })

    except ObjectDoesNotExist:
        error_message = "The listing requested does not exist."
        return render(request, "auctions/error.html", {
            "message": error_message
        })


@login_required
def add_watchlist(request, listing_id):

    # If the listing is already in the watchlist, delete it.
    try:
        listing = Watchlist.objects.get(item=listing_id)
        listing.delete()
        messages.success(request, "item deleted!")

    # If not, add it.
    except ObjectDoesNotExist:
        listing = Listing.objects.get(pk=listing_id)
        watchlist = Watchlist(item=listing, user=request.user)
        watchlist.save()
        messages.success(request, "item added to watchlist successfully!")

    display = Listing.objects.get(pk=listing_id)

    return HttpResponseRedirect(reverse("display", args=[display.id]))


# Function for saving and updating data to ModelForms.
def save_and_update(data, new_price_listing, request):
    data.user = request.user
    data.item = new_price_listing
    data.save()
    new_price_listing.starting_bid = data.bidding
    new_price_listing.save()
    messages.success(request, "You bid beautifully!")


@login_required
def add_bidding(request, listing_id):
    if request.method == "POST":

        # Check and save ModelForm.
        form = BiddingForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            new_price_listing = Listing.objects.get(pk=listing_id)

            # If there is a bidding already, the new bidding has to be greater.
            if Bidding.objects.filter(item=listing_id).last() is not None:

                if data.bidding > new_price_listing.starting_bid:
                    save_and_update(data, new_price_listing, request)
                else:
                    messages.success(request, "Please bid a bigger sum!")

            # If there is no bidding yet, the new bidding should be at least equal to the starting bid.
            else:
                if data.bidding >= new_price_listing.starting_bid:
                    save_and_update(data, new_price_listing, request)
                else:
                    messages.success(request, "Please bid a bigger sum!")

            return HttpResponseRedirect(reverse("display", args=[new_price_listing.id]))

        else:
            error_message = "Input is not valid."
            return render(request, "auctions/error.html", {
                "message": error_message
            })


@login_required
def close_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.activity = False
    listing.save()
    return HttpResponseRedirect(reverse("display", args=[listing.id]))


@login_required
def add_comment(request, listing_id):
    if request.method == "POST":

        # Check and save ModelForm.
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            listing = Listing.objects.get(pk=listing_id)
            data.item = listing
            data.save()
            return HttpResponseRedirect(reverse("display", args=[data.item.id]))
        else:
            error_message = "Input is not valid."
            return render(request, "auctions/error.html", {
                "message": error_message
            })


@login_required
def watchlist(request):

    # Check if there are listings in the watchlist.
    try:
        watchlist = Watchlist.objects.filter(user=request.user).order_by("-id")
    except EmptyResultSet:
        watchlist = None
    return render(request, "auctions/watchlist.html", {
        "listings": watchlist
    })


def list_categories(request):

    # Check if there yet exists any category.
    try:
        listings = Listing.objects.values("category").distinct()
    except EmptyResultSet:
        listings = None
    return render(request, "auctions/categories.html", {
        "listings": listings
    })


def list_category(request, category):

    # Check if there are listings in the category.
    try:
        listings = Listing.objects.filter(category=category, activity=True).order_by("-id")
    except EmptyResultSet:
        listings = None

    header = "Listings belong to this category"
    return render(request, "auctions/index.html", {
        "listings": listings,
        "header": header
    })


def display_closed_listings(request):

    # Check if there are closed listings.
    try:
        listings = Listing.objects.filter(activity=False).order_by("-id")
    except EmptyResultSet:
        listings = None

    header = "Closed Listings"
    return render(request, "auctions/index.html", {
        "listings": listings,
        "header": header
    })
