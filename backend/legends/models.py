from django.db import models
from django.utils.text import slugify


class Legend(models.Model):
    slug = models.SlugField(max_length=120, unique=True, primary_key=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, default='')
    biography = models.TextField(blank=True, default='')
    lang = models.CharField(max_length=10, default='en')

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name