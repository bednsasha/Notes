from django.contrib import admin
from .models import  Category, Note

admin.site.register(Note)
admin.site.register(Category)