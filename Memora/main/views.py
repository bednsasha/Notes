from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Note

def page_not_found(request,exception):
    return render(request, '404.html', status=404)

def index(request):
    return HttpResponse("It's a main page")

def notes (request,note_name):
    return HttpResponse(f'<h1>NOTE</h1><p>Note name: {note_name}</p>')

def authorization(request):
    return render(request, 'authorization.html')

def registration(request):
    return render(request, 'registration.html')
def password_change(request):
    return render(request, 'password_change.html')