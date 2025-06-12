from django.db import models
from django.urls import reverse
from django.utils.text import slugify

   
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=True, default='Noname')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = 'Noname'
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Note(models.Model):
    title = models.CharField(max_length=200, blank=True, default='Noname')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    favourites = models.BooleanField(default=False)
    in_basket = models.BooleanField(default=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
            # Генерируем slug из title, можно добавить проверку на уникальность при необходимости
            self.slug = slugify(self.title)
        if not self.category:
            # Если хотите, чтобы при отсутствии категории всегда ставился Category с названием 'Noname', можно создать или получить её
            default_category, created = Category.objects.get_or_create(name='Noname')
            self.category = default_category
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})
