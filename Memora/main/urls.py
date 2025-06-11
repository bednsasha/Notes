from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name='home'),
    path('authorization/', views.authorization, name='authorization'),
    path('registration/', views.registration, name='registration'),
    path('password_change/', views.password_change, name='password_change'),
    path('code/', views.code, name='code'),
    path('notes/', views.add_note, name='add_note'),
    path('notes/<slug:slug>/', views.edit_note, name='edit_note'),
    path('folder/', views.categories, name='category'),
    path('folder/<slug:slug_cat>', views.certain_categories, name='certain_category'),
    path('basket/', views.basket, name='basket'),
    path('basket/<int:note_id>', views.list_basket, name='list_basket'),
    path('delete_note/<int:note_id>/', views.delete_note, name='delete_note'),
    path('favourites/', views.favourites, name='favourites'),
    path('favourites/<int:note_id>', views.list_fav, name='list_fav'),
    path('note(style)/', views.Add_note, name='note_style'),
    path('folder/<int:pk>/edit/', views.CategoryEditView.as_view(), name='category_edit'),

    
]