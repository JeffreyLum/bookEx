from django.contrib import admin

from .models import MainMenu
from .models import Announcement
from .models import Book
from .models import Cart
from .models import Wish

admin.site.register(MainMenu)
admin.site.register(Announcement)
admin.site.register(Book)
admin.site.register(Cart)
admin.site.register(Wish)
