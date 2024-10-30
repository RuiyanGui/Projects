from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listing/<int:listing_id>", views.display_listing, name="display"),
    path("watchlist/<int:listing_id>", views.add_watchlist, name="add_watchlist"),
    path("bid/<int:listing_id>", views.add_bidding, name="bidding"),
    path("close/<int:listing_id>", views.close_listing, name="close"),
    path("comment?<int:listing_id>", views.add_comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.list_categories, name="categories"),
    path("category/<str:category>", views.list_category, name="category"),
    path("closed_listings", views.display_closed_listings, name="closed")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
