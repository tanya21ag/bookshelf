from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Pileofbooks

def index(request):
  mybooks = Pileofbooks.objects.all().values()
  template = loader.get_template('index.html')
  context = {
    'mybooks': mybooks,
  }
  return HttpResponse(template.render(context, request))

def add(request):
   template = loader.get_template('add.html')
   return HttpResponse(template.render({}, request))

def addrecord(request):
  x = request.POST['title']
  y = request.POST['author']
  book1 = Pileofbooks(title=x, author=y)
  book1.save()
  return HttpResponseRedirect(reverse('index'))

def delete(request, id):
  book2 = Pileofbooks.objects.get(id=id)
  book2.delete()
  return HttpResponseRedirect(reverse('index'))

def update(request, id):
  mybook = Pileofbooks.objects.get(id=id)
  template = loader.get_template('update.html')
  context = {
    'mybook': mybook,
  }
  return HttpResponse(template.render(context, request))

def updaterecord(request, id):
  first = request.POST['title']
  last = request.POST['author']
  book3 = Pileofbooks.objects.get(id=id)
  book3.title = first
  book3.author = last
  book3.save()
  return HttpResponseRedirect(reverse('index'))