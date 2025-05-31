from django.db import models
from django.urls import reverse

class Note(models.Model):
    name=models.CharField(max_length=200)
    text = models.TextField(blank=True, null=True)
    slug=models.SlugField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        ordering = ('name',)
       
    def __str__(self):
        return self.name
    
def get_absolute_url(self):
    return reverse('main:note_detail',
                   args=[self.slug])
