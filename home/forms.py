from django import forms
from .models import Book
from .models import ReadingProgress

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_date']

class ReadingProgressForm(forms.ModelForm):
    class Meta:
        model = ReadingProgress
        fields = ['page_number']