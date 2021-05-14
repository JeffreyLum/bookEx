from django.db import models

from django.contrib.auth.models import User



class MainMenu(models.Model):
    item = models.CharField(max_length=200, unique=True)
    link = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.item


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=500)
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    post_date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.title)


class Book(models.Model):
    name = models.CharField(max_length=200)
    web = models.URLField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    publishdate = models.DateField(auto_now=True)
    picture = models.FileField(upload_to='bookEx/static/uploads', blank=False)
    pic_path = models.CharField(max_length=300, editable=False, blank=True)
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.name)


class BookSearch(models.Model):
    name = models.CharField(max_length=200, primary_key=True, default="")

    def __str__(self):
        return str(self.name)


class Cart(models.Model):
    seller_book_id = models.IntegerField()
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class Wish(models.Model):
    bookName = models.CharField("Book Name", max_length=200)
    theUser = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.bookName)

