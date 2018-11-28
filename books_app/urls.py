from django.urls import path, include

from books_app import views

urlpatterns = [
    path('main/', views.index, name='main'),
    path('details/', views.details, name='details'),
    path('bookList/', views.book_list, name='bookList'),
]
