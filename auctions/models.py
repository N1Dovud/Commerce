from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    title = models.CharField(max_length=64, unique=True, null=False, blank=False)
    description = models.CharField(max_length=1024, null=False, blank=False)
    starting_bid = models.DecimalField(max_digits=7, decimal_places=2, blank=False, null=False)
    highest_bid = models.DecimalField(max_digits=7, decimal_places=2, blank=False, null=False)
    image = models.URLField(blank=True, null=True)
    time = models.CharField(max_length=32, null=False, blank=False)
    CATEGORY_CHOICES = [
        ("books", "Books"),
        ("technology", "Technology"),
        ("appliances", "Appliances"),
        ("clothes", "Clothes"),
        ("accessories", "Accessories"),
    ]
    category = models.CharField(blank=True, max_length=64, choices=CATEGORY_CHOICES, null=False)
    closed = models.BooleanField(default=False)

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=False, null=False, related_name="bids")
    bid_amount = models.DecimalField(max_digits=7, decimal_places=2,blank=False, null=False)
    bid_number = models.PositiveIntegerField(blank=False, null=False, default=1)


class Comment(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=False, null=False, related_name="comments")
    comment = models.CharField(max_length=512, null=False, blank=True)


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    watchlist = models.ManyToManyField(Listing,blank=True, related_name="watchlists")