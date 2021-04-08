from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('postbook', views.postbook, name='postbook'),  # clicking Post Book redirects to here
    path('displaybooks', views.displaybooks, name='displaybooks'),  # clicking Display Books redirects to here
    path('aboutus', views.aboutus, name='aboutus'),
    path('wishlist', views.wishlist, name='wishlist'),
]