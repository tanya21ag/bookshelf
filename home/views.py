from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from home.models import Contact
from django.contrib import messages
from .models import Book, ReadingProgress
from .forms import BookForm
from .forms import ReadingProgressForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def faq(request):
    return render(request, 'faq.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        query = request.POST.get('query')
        contact = Contact(name=name, email=email, query=query)
        contact.save()
        messages.success(request, "Your query has been sent.")
    return render(request, 'contact.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('bookshelf'))
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('bookshelf'))
            else:
                # Handle authentication failure
                pass
        else:
            # Handle missing 'username' or 'password' fields in the POST data
            pass

    return render(request, 'registration/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

def landing(request):
    return render(request, 'registration/landing.html')

@login_required
def bookshelf(request):
    user = request.user
    reading_list = Book.objects.filter(user=user)
    reading_progress = ReadingProgress.objects.filter(user=user)
    return render(request, 'bookshelf.html', {'reading_list': reading_list, 'reading_progress': reading_progress})

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            user = request.user
            book = form.save(commit=False)
            book.user = user
            book.save()
            progress = ReadingProgress(book=book, page_number=0, user=user)
            progress.save()
    return redirect('bookshelf')

@require_POST
def update_progress(request, book_id):
    user = request.user
    page_number = request.POST.get('page_number')
    book = Book.objects.get(id=book_id)
    reading_progress, created = ReadingProgress.objects.get_or_create(user=user, book=book)
    reading_progress.page_number = page_number
    reading_progress.save()
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        response_data = {'message': 'Progress updated successfully'}
        return JsonResponse(response_data)
    else:
        return redirect('bookshelf')

def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        book.delete()
    return redirect('bookshelf')
