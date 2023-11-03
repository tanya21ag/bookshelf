from django.urls import path
from home import views

urlpatterns = [
    path("", views.home, name='home'),
    path("about/", views.about, name='about'),
    path("faq/", views.faq, name='faq'),
    path("contact", views.contact, name='contact'),
    path("register/", views.register, name='register'),
    path("login/", views.user_login, name='login'),
    path("logout/", views.user_logout, name='logout'),
    path("landing/", views.landing, name='landing'),
    path("bookshelf/", views.bookshelf, name='bookshelf'),
    path('add_book/', views.add_book, name='add_book'),
    path('update_progress/<int:book_id>/', views.update_progress, name='update_progress'),
]
