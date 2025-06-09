from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('authorization/', views.authorization, name='authorization'),
    path('registration/', views.registration, name='registration'),
    path('password_change/', views.password_change, name='password_change'),
    path('code/', views.code, name='code'),
    path('notes/', views.add_note, name='add_note'),
    path('notes/<slug:slug>/', views.edit_note, name='edit_note'),
    path('category/', views.categories, name='category'),
    path('category/<slug:slug_cat>', views.certain_categories, name='certain_category'),
    path('basket/', views.basket, name='basket'),
    path('basket/<int:note_id>', views.list_basket, name='list_basket'),
    path('delete_note/<int:note_id>/', views.delete_note, name='delete_note'),
    path('favourites/', views.favourites, name='favourites'),
    path('favourites/<int:note_id>', views.list_fav, name='list_fav'),
    path('main/', views.main, name='main'),

 
]