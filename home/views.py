from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.shortcuts import render, redirect
from home.models import Contact
from django.contrib import messages
from datetime import datetime
from .models import Book, ReadingProgress
from .forms import BookForm
from .forms import ReadingProgressForm

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
        contact = Contact(name=name, email=email, query=query, date=datetime.today())
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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('bookshelf'))
        else:
            # Handle login failure (e.g., display an error message)
            pass
    return render(request, 'registration/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

def landing(request):
    return render(request, 'registration/landing.html')

def bookshelf(request):
    user = request.user
    reading_list = Book.objects.filter(user=user)
    reading_progress = ReadingProgress.objects.filter(user=user)

    return render(request, 'bookshelf.html', {'reading_list': reading_list, 'reading_progress': reading_progress})


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user  # Assign the current user to the book
            book.save()
            return redirect('bookshelf')  # Redirect to the bookshelf page
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})


def update_progress(request, book_id):
    book = Book.objects.get(pk=book_id)
    if book.user == request.user:  # Check if the book belongs to the current user
        if request.method == 'POST':
            form = ReadingProgressForm(request.POST, instance=book.readingprogress)
            if form.is_valid():
                form.save()
                return redirect('bookshelf')  # Redirect to the bookshelf page
        else:
            form = ReadingProgressForm(instance=book.readingprogress)
        return render(request, 'update_progress.html', {'form': form, 'book': book})
    else:
        return HttpResponseForbidden("You don't have permission to update this book's progress.")
