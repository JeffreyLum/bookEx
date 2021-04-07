from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import MainMenu
from .forms import BookForm
from django.http import HttpResponseRedirect
from .models import Book

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


def index(request):
    return render(
        request,
        'bookMng/index.html',
        {
          'item_list': MainMenu.objects.all() # the items in Main Menus in /admin
        },
    )


def postbook(request):
    submitted = False
    if request.method == 'POST':
        # automatically links them together
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save() # saves to database
            return HttpResponseRedirect('/postbook?submitted=True') # if everything works out, then will submit
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


def aboutus(request):
    return render(
        request,
        'bookMng/aboutus.html',
        {
            'item_list': MainMenu.objects.all(),
        },
    )


class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)

