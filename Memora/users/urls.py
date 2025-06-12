from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name='users'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    path('registration/', views.registration, name='registration'),
    path('password_change/', views.password_change, name='password_change'),
    
    
    ]
