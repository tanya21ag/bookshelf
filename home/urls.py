from django.urls import path
from home import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.home, name='home'),
    path("about/", views.about, name='about'),
    path("contact", views.contact, name='contact'),
    path("register/", views.register, name='register'),
    path("login/", views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path("landing/", views.landing, name='landing'),
    path("bookshelf/", views.bookshelf, name='bookshelf'),
    path('add_book/', views.add_book, name='add_book'),
    path('update_progress/<int:book_id>/', views.update_progress, name='update_progress'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),

]
