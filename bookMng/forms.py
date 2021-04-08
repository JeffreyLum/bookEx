from django import forms
from django.forms import ModelForm
from .models import Book
from .models import Wish

# User Input
class BookForm(ModelForm):
    # inner class
    class Meta:
        model = Book
        fields = [
            'name',
            'web',
            'price',
            'picture'
        ]

class WishForm(ModelForm):
    class Meta:
        model = Wish
        exclude = ['wished_by']