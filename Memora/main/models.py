from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
    
    def __str__(self):
        return self.name

class Note(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    favourites = models.BooleanField(default=False, blank=True) 
    in_basket=models.BooleanField(default=False, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='notes', null=True, blank=True)  
    class Meta:
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"
        ordering = ('title',)

    def __str__(self):
        return self.title[0:50]
    
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

