from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('search/', views.book_search, name='book_search'),
    path('create/', views.book_create, name='book_create'),
    path('<slug:slug>/', views.book_detail, name='book_detail'),
    path('<slug:slug>/edit/', views.book_edit, name='book_edit'),
    path('<slug:slug>/update/', views.book_update, name='book_update'),
    path('<slug:slug>/delete/', views.book_delete, name='book_delete'),
    path('<slug:slug>/preview/', views.book_preview, name='book_preview'),
]
