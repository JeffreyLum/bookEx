from django import forms
from django.forms import ModelForm
from .models import Book


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