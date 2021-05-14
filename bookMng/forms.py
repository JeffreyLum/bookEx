from django import forms
from django.forms import ModelForm

from .models import Announcement
from .models import Book
from .models import BookSearch
from .models import Cart
from .models import Wish


class AnnouncementForm(ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            'name',
            'web',
            'price',
            'picture',
        ]


class CartForm(ModelForm):
    class Meta:
        model = Cart
        fields = ['seller_book_id']


class SearchForm(ModelForm):
    class Meta:
        model = BookSearch
        fields = ['name']


class WishForm(ModelForm):
    class Meta:
        model = Wish
        fields = ['bookName']
