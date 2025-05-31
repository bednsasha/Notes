from django.shortcuts import render, get_object_or_404
from .models import Note

def page_not_found(request,exception):
    return render(request, '404.html', status=404)
    

