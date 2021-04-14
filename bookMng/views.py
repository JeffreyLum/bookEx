from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import MainMenu
from .forms import BookForm
from .forms import WishForm
from django.http import HttpResponseRedirect
from .models import Book
from .models import Wish
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required

def index(request):
    return render(
        request,
        'bookMng/index.html',
        {
          'item_list': MainMenu.objects.all() # the items in Main Menus in /admin
        },
    )


@login_required(login_url=reverse_lazy('login'))
def postbook(request):
    submitted = False
    if request.method == 'POST':
        # automatically links them together
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            #form.save() # saves to database
            book = form.save(commit=False)  # Commit means save to database, 'False' means we dont want to save yet
            try:
                book.username = request.user
            except Exception:
                pass  # Don't do anythin
            book.save()
            return HttpResponseRedirect('/postbook?submitted=True')  # if everything works out, then will submit
    else:
        form = BookForm() # deletes empty form when someone clicks postbook
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
                  'bookMng/postbook.html',
                  {
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'submitted': submitted
                  })


@login_required(login_url=reverse_lazy('login'))
def displaybooks(request):
    books = Book.objects.all()
    for b in books:
        b.pic_path = b.picture.url[14:]
        # is 14 because it gets the path /static/uploads/[THE IMAGES], 14 characters from static
    return render(request,
                  'bookMng/displaybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  })

def wishlist(request):

    if request.method == 'POST':
        form = WishForm(request.POST)
        if form.is_valid():
            form_2 = form.save(commit=False)
            form_2.wished_by = request.POST.get('person')
            form_2.save()
            return HttpResponseRedirect('/wishlist')
    else:
        form = WishForm()
    return render(
        request,
        'bookMng/wishlist.html',
        {
            'form': form,
            'item_list': MainMenu.objects.all(),
            'wish_list': Wish.objects.all(),
        })

def aboutus(request):
    return render(
        request,
        'bookMng/aboutus.html',
        {
            'item_list': MainMenu.objects.all(),
        },
    )


@login_required(login_url=reverse_lazy('login'))
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    book.pic_path = book.picture.url[14:]  # is 14 because it gets the path /static/uploads/[THE IMAGES], 14 characters from static
    return render(request,
                  'bookMng/book_detail.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book
                  })


class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)

