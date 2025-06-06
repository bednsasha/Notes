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
    path('category/<slug:slug_cat>', views.categories, name='category'),

 
]