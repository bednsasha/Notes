from django.db import models
from django.urls import reverse


class Note(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Заметки"
        verbose_name_plural = "Заметки"
        ordering = ('title',)

    def __str__(self):
        return self.title[0:50]
    
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

