from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<str:title>", views.listing_page, name="listing_page"),
    path("closed_listing/<str:title>", views.closed_listing, name="closed_listing"),
    path("closed_listings", views.closed_listings, name="closed_listings"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories/<str:category>", views.categories, name="categories")
]
