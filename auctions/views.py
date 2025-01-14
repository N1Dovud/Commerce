from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime 
from .forms import ListingForm
from .models import User, Listing, Bid, Comment, Watchlist
from decimal import Decimal
from django.contrib import messages


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(closed=False)
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
def create(request):
    # if a user send information about the listing
    if request.method == "POST" and request.user.is_authenticated:
        try:
            # create all the necessary fields and store them
            title = request.POST["title"]
            description = request.POST["description"]
            starting_bid = request.POST["starting_bid"]
            image = request.POST["image_url"]
            form = ListingForm(request.POST)
            if form.is_valid():
                category = form.cleaned_data["category"]
            time = datetime.now().strftime("%b %d, %Y, %I:%M %p")
            listing = Listing.objects.create(user=request.user, title=title, highest_bid=starting_bid, description=description, starting_bid=starting_bid, image=image,time=time, category=category)
            bid = Bid.objects.create(user=request.user, listing=listing, bid_amount=starting_bid)
            listing.save()
            bid.save()
            messages.success(request, "Successfully created!!")
            return redirect("index")
            # display a message
        except Exception as e:
            messages.error(request, e)
            return render(request, "auctions/create.html")
    else:
        form = ListingForm()
        return render(request, "auctions/create.html",{
            "form": form
        })
    
def listing_page(request, title):

    # if a user sends a form
    if request.method == "POST":
        # if a user is logged in
        if request.user.is_authenticated:
            # get the needed listing
            listing = Listing.objects.get(title=title)
            # if the user is the creator of the listing and wanted to close it
            if request.user == Listing.objects.get(title=title).user and "close" in request.POST:
                listing.closed = True
                listing.save()
                messages.success(request, f"You closed your listing called '{listing.title}'")
                return redirect("closed_listing", title=title)
            # removing or adding to a watchlist
            elif "watchlist" in request.POST:
                watchlist_list = request.POST.get("watchlist") 
                watchlist, created = Watchlist.objects.get_or_create(user=request.user)
                # adding to a watchlist
                if watchlist_list == "add":
                    watchlist.watchlist.add(listing)
                # removing from a watchlist
                elif watchlist_list == "remove":
                    watchlist_entry = Watchlist.objects.get(user=request.user, watchlist=listing)
                    watchlist_entry.watchlist.remove(listing)
                return redirect("listing_page", title=listing.title)
            # if a bid is placed
            elif "bid" in request.POST:
                bid = Decimal(request.POST.get("bid"))
                # if bid is valid
                if bid > listing.highest_bid:
                    bid_number = Bid.objects.get(bid_amount=listing.highest_bid, listing=listing).bid_number + 1
                    listing.highest_bid = bid
                    listing.save()
                    bidding = Bid.objects.create(user=request.user, bid_amount=bid, bid_number=bid_number, listing=listing)
                    bidding.save()
                    messages.success(request, "Successfully placed a bid")
                    return redirect("listing_page", title=listing.title)
                else:
                    messages.error(request, "Bid was not added, make a higher bid")
                    return redirect("listing_page", title=listing.title)
            # if a user made a comment
            elif "comment" in request.POST:
                comment = request.POST.get("comment")
                if comment:
                    new_comment= Comment.objects.create(user=request.user, listing=listing, comment=comment)
                    new_comment.save()
                    messages.success(request, "your comment is added!")
                else:
                    messages.error(request, "Comment should not be empty!")
                return redirect("listing_page", title=listing.title)
        else:
            messages.error(request, "Please, login first!")
            return redirect("auctions/login.html")
    # if a user tries to go to a listing page
    if request.method == "GET":
        # get necessary data to send to the template
        listing = Listing.objects.get(title=title)
        comments = Comment.objects.filter(listing=listing)
        message = request.GET.get("message","")
        bid_number = Bid.objects.get(listing=listing, bid_amount=listing.highest_bid).bid_number
        # if user is logged in
        if request.user.is_authenticated:
            watchlist = Watchlist.objects.filter(user=request.user, watchlist=listing).exists()
            # if the highest bid is made by the user
            if request.user == Bid.objects.get(listing=listing, bid_amount=listing.highest_bid).user:
                current = True
            else:
                current = False
            # if the user is the creator of the listing
            if request.user.is_authenticated and request.user == Listing.objects.get(title=title).user:
                return render(request, "auctions/listing.html", {
                    "creator": True,
                    "listing": listing,
                    "comments": comments,
                    "watchlisted": watchlist,
                    "current": current,
                    "message": message,
                    "bid_number": bid_number
                })
            else:
                return render(request, "auctions/listing.html",{
                    "listing": listing,
                    "comments": comments,
                    "watchlisted": watchlist,
                    "current": current,
                    "message": message,
                    "bid_number": bid_number
                })
        # if the user is not logged in
        else:
            return render(request, "auctions/listing.html",{
                    "listing": listing,
                    "comments": comments,
                    "current": False,
                    "bid_number": bid_number,
                })

def closed_listing(request, title):
    # if a form is sent
    if request.method == "POST":
        "if logged in"
        if request.user.is_authenticated:
            # get the data related to the listing
            listing = Listing.objects.get(title=title)
            # adding or removing from a watchlist
            if "watchlist" in request.POST:
                watchlist_list = request.POST.get("watchlist") 
                watchlist, created = Watchlist.objects.get_or_create(user=request.user)
                # adding
                if watchlist_list == "add":
                    watchlist.watchlist.add(listing)
                # removing
                elif watchlist_list == "remove":
                    watchlist_entry = Watchlist.objects.get(user=request.user, watchlist=listing)
                    watchlist_entry.watchlist.remove(listing)
                return redirect("closed_listing", title=listing.title)
            #in case the user makes a new comment
            elif "comment" in request.POST:
                comment = request.POST.get("comment")
                if comment:
                    new_comment= Comment.objects.create(user=request.user, listing=listing, comment=comment)
                    new_comment.save()
                    messages.success(request, "your comment is added!")
                else:
                    messages.error(request, "Comment should not be empty!")
                return redirect("closed_listing", title=listing.title)
        else:
            #if the user is not logged in
            messages.error(request, "Please, login first!")
            return redirect("login")
    "if a user tries to go to a listing page"
    if request.method == "GET":
        # get all the necessary data
        listing = Listing.objects.get(title=title)
        comments = Comment.objects.filter(listing=listing)
        bid_number = Bid.objects.get(bid_amount=listing.highest_bid,listing=listing).bid_number
        # if the user is signed in
        if request.user.is_authenticated:
            # if the user is also the winner of the auction
            watchlist = Watchlist.objects.filter(user=request.user, watchlist=listing).exists()
            if request.user.is_authenticated and request.user == Bid.objects.get(bid_amount=listing.highest_bid, listing=listing).user:
                return render(request, "auctions/closed_listing.html", {
                    "listing": listing,
                    "comments": comments,
                    "watchlisted": watchlist,
                    "message": "You won the auction! Congrats!!!!",
                    "bid_number": bid_number
                })
            else:
                return render(request, "auctions/closed_listing.html",{
                    "listing": listing,
                    "comments": comments,
                    "watchlisted": watchlist,
                    "bid_number": bid_number
                })
        # if the user is not logged in
        else:
            return render(request, "auctions/closed_listing.html",{
                    "listing": listing,
                    "comments": comments,
                    "bid_number": bid_number,
                })

def closed_listings(request):
    # hands back all the closed listings
    listings = Listing.objects.filter(closed=True)
    return render(request, "auctions/closed_listings.html", {
        "listings": listings
    })


def watchlist(request):
    # shows the watchlist of the user
    watchlist_entries = Watchlist.objects.filter(user=request.user, watchlist__isnull=False)
    if watchlist_entries.exists():
        listings = Listing.objects.filter(watchlists__user=request.user)
        return render(request, "auctions/watchlist.html", {
            "listings": listings
        })
    else:
        return render(request, "auctions/watchlist.html", {
            "listings": ""
        })


def categories(request, category):
    # displays listings of particular category
    if category in dict(Listing.CATEGORY_CHOICES).keys():
        listings = Listing.objects.filter(category=category,closed=False)
        category = category.capitalize()
        return render(request, "auctions/categories.html", {
            "listings": listings,
            "category":category
        })
    elif category == "uncategorized":
        listings = Listing.objects.filter(category="", closed=False)
        category = category.capitalize()
        return render(request, "auctions/categories.html", {
            "listings": listings,
            "category":category
        })
