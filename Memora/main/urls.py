from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name='home'),
    path('notes/', views.add_note, name='add_note'),
    path('notes/<slug:slug>/', views.edit_note, name='edit_note'),
    path('folder/', views.categories, name='category'),
    path('folder/<slug:slug_cat>', views.certain_categories, name='certain_category'),
    path('add_folder/', views.add_folder, name='add_folder'),
    path('basket/', views.basket, name='basket'),
    path('basket/<int:note_id>', views.list_basket, name='list_basket'),
    path('delete_note/<int:note_id>/', views.delete_note, name='delete_note'),
    path('favourites/', views.favourites, name='favourites'),
    path('favourites/<int:note_id>', views.list_fav, name='list_fav'),
    path('folder/<int:pk>/edit/', views.CategoryEditView.as_view(), name='category_edit'),

    
]