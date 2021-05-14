from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import MainMenu
from .models import Announcement
from .models import Book
from .models import Cart
from .models import Wish
from .forms import AnnouncementForm
from .forms import BookForm
from .forms import CartForm
from .forms import SearchForm
from .forms import WishForm

from random import randint


def index(request):
    num_of_announces = 3
    num_of_books = 4

    books_count = Book.objects.count()

    books = Book.objects.all()[(books_count - num_of_books):]
    for b in books:
        b.pic_path = b.picture.url[14:]

    return render(request,
                  'bookMng/index.html',
                  {
                      'title': "Home",
                      'header': "Welcome to Book Exchange System",
                      'item_list': MainMenu.objects.all(),
                      'announces': Announcement.objects.order_by('-id')[:num_of_announces],
                      'cart_size': Cart.objects.filter(user=request.user.id).count(),
                      'books': books
                  })


def aboutus(request):
    return render(request,
                  'bookMng/aboutus.html',
                  {
                      'title': "About Us",
                      'item_list': MainMenu.objects.all(),
                      'cart_size': Cart.objects.filter(user=request.user.id).count()
                  })


def announcements(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.username = request.user
            a.save()
            return HttpResponseRedirect('/announcements')
    else:
        form = AnnouncementForm()

    return render(request,
                  'bookMng/announcements.html',
                  {
                      'title': "Announcements",
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'announces': Announcement.objects.order_by('-id'),
                      'cart_size': Cart.objects.filter(user=request.user.id).count()
                  })


@login_required(login_url=reverse_lazy('login'))
def book_delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return render(request,
                  'bookMng/book_delete.html',
                  {
                      'title': "Book Delete",
                      'item_list': MainMenu.objects.all(),
                      'book': book,
                      'cart_size': Cart.objects.filter(user=request.user.id).count()
                  })


@login_required(login_url=reverse_lazy('login'))
def book_detail(request, book_id):
    uid = request.user.id
    book = Book.objects.get(id=book_id)

    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.user = request.user
            a.seller_book_id = book_id
            a.save()
            return HttpResponseRedirect('/cart')
    else:
        form = CartForm()
    
    book.pic_path = book.picture.url[14:]
    return render(request,
                  'bookMng/book_detail.html',
                  {
                      'title': "Book Details",
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'book': book,
                      'cart_size': Cart.objects.filter(user=uid).count(),
                      'cart_items': list(Cart.objects.filter(user=uid).values_list('seller_book_id'))
                  })


@login_required(login_url=reverse_lazy('login'))
def book_search(request, searched=""):

    submitted = False
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.name = request.POST.get('name')
            return HttpResponseRedirect('/book_search?q=' + a.name)
    else:
        form = SearchForm()
        if 'q' in request.GET:
            searched = request.GET.get('q', '')
            submitted = True

    books = Book.objects.filter(name__icontains=searched)
    for b in books:
        b.pic_path = b.picture.url[14:]

    return render(request, 'bookMng/book_search.html',
                  {
                      'title': "Book Search",
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                      'submitted': submitted,
                      'form': form,
                      'searched': searched,
                      'cart_size': Cart.objects.filter(user=request.user.id).count()
                  })


@login_required(login_url=reverse_lazy('login'))
def cart(request):
    uid = request.user.id

    if request.method == 'POST':
        item_to_remove = Cart.objects.filter(user=uid).get(seller_book_id=request.POST.get('to_remove'))
        item_to_remove.delete()
        return HttpResponseRedirect('/cart')

    the_cart = [book_ids for book_ids, in Cart.objects.filter(user=uid).values_list('seller_book_id')]
    total_price = 0

    books = []
    for cart_id in the_cart:
        book = Book.objects.get(id=cart_id)
        total_price += book.price
        books.append(book)

    for b in books:
        b.pic_path = b.picture.url[14:]

    return render(request,
                  'bookMng/cart.html',
                  {
                      'title': "Cart",
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                      'cart_size': Cart.objects.filter(user=uid).count(),
                      'total_price': total_price
                  })


@login_required(login_url=reverse_lazy('login'))
def checkout(request):
    uid = request.user.id
    cart_book_ids = [book_ids for book_ids, in Cart.objects.filter(user=uid).values_list('seller_book_id')]

    if request.method == 'POST':
        for cart_id in cart_book_ids:
            book = Book.objects.get(id=cart_id)
            book.username_id = uid
            book.save()
            Cart.objects.filter(seller_book_id=cart_id).delete()

        return HttpResponseRedirect('/checkout')

    total_price = 0

    books = []
    for cart_id in cart_book_ids:
        book = Book.objects.get(id=cart_id)
        total_price += book.price
        books.append(book)

    for b in books:
        b.pic_path = b.picture.url[14:]

    return render(request,
                  'bookMng/checkout.html',
                  {
                      'title': "Checkout",
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                      'cart_size': Cart.objects.filter(user=uid).count(),
                      'total_price': total_price
                  })


@login_required(login_url=reverse_lazy('login'))
def displaybooks(request):
    books = Book.objects.all()
    for b in books:
        b.pic_path = b.picture.url[14:]

    return render(request,
                  'bookMng/displaybooks.html',
                  {
                      'title': "Display Books",
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                      'cart_size': Cart.objects.filter(user=request.user.id).count()
                  })


@login_required(login_url=reverse_lazy('login'))
def mybooks(request):
    books = Book.objects.filter(username=request.user)
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookMng/mybooks.html',
                  {
                      'title': "My Books",
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                      'cart_size': Cart.objects.filter(user=request.user.id).count()
                  })


@login_required(login_url=reverse_lazy('login'))
def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            try:
                book.username = request.user
            except Exception:
                pass
            book.save()
            return HttpResponseRedirect('/postbook?submitted=True')
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request,
                  'bookMng/postbook.html',
                  {
                      'title': "Post Book",
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'submitted': submitted,
                      'cart_size': Cart.objects.filter(user=request.user.id).count()
                  })


@login_required(login_url=reverse_lazy('login'))
def suprise_book(request):

    num_of_books = Book.objects.count()
    ran = randint(1, num_of_books) - 1

    book = Book.objects.all()[ran]
    book.pic_path = book.picture.url[14:]

    return render(request, 'bookMng/suprise_book.html',
                  {
                      'title': "Surprise Book",
                      'item_list': MainMenu.objects.all(),
                      'book': book,
                      'cart_size': Cart.objects.filter(user=request.user.id).count()
                  })


@login_required(login_url=reverse_lazy('login'))
def wishlist(request):
    if request.method == 'POST':
        form = WishForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.theUser = request.user
            a.save()
            return HttpResponseRedirect('/wishlist')
    else:
        form = WishForm()
    return render(request,
                  'bookMng/wishlist.html',
                  {
                    'title': "Wish List",
                    'form': form,
                    'item_list': MainMenu.objects.all(),
                    'wish_list': Wish.objects.all(),
                    'cart_size': Cart.objects.filter(user=request.user.id).count()
                  })


class Register(CreateView):

    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)
