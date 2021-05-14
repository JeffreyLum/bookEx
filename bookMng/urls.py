from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('announcements', views.announcements, name='announcements'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('book_detail/<int:book_id>', views.book_detail, name='book_detail'),
    path('book_delete/<int:book_id>', views.book_delete, name='book_delete'),
    path('book_search', views.book_search, name='book_search'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('displaybooks', views.displaybooks, name='displaybooks'),
    path('mybooks', views.mybooks, name='mybooks'),
    path('postbook', views.postbook, name='postbook'),
    path('suprise_book', views.suprise_book, name='suprise_book'),
    path('wishlist', views.wishlist, name='wishlist')
]
