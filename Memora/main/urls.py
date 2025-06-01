from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('authorization/',views.authorization, name='authorization'),
    path('registration/',views.registration, name='registration'),
    path('password_change/',views.registration, name='password_change'),
    path('Notes/<path:note_name>/', views.notes, name='note'),
]