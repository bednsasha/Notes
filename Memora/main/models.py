from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings
from django.contrib.auth.models import User

class ApplicantProfile(models.Model):
    name = models.CharField(max_length = 50)
    confirmation_code = models.CharField(max_length=4, blank=True)
    email = models.EmailField()
    is_active=models.BooleanField(default=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code_created_at = models.DateTimeField(null=True, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, default='Noname')  
    slug = models.SlugField(max_length=255, blank=True, db_index=True)
    owner = models.ForeignKey(ApplicantProfile, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        unique_together = ('slug', 'owner')  # слаг уникален в рамках владельца

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = 'Noname'
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug, owner=self.owner).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)



class Note(models.Model):
    title = models.CharField(max_length=200, blank=True, default='Noname')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    favourites = models.BooleanField(default=False)
    in_basket = models.BooleanField(default=False)
    owner = models.ForeignKey(ApplicantProfile, on_delete=models.CASCADE,)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='notes',
        null=True,
        blank=True,
        default=None
    )
    class Meta:
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"
        ordering = ('title',)
    def __str__(self):
        return self.title[0:50]
    def save(self, *args, **kwargs):
        if not self.title:
            self.title = 'Noname'
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.category:
            default_category, created = Category.objects.get_or_create(
                name='Noname',
                owner=self.owner  
            )
            self.category = default_category
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})
