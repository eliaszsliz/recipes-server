from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=63)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

class Recipe(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    image = models.ImageField()
    body = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='recipes')
    favourites = models.ManyToManyField(User, related_name='favoured')

    DIFFICULTY_CHOICES = (
        ('easy', 'Easy'),
        ('medium', 'Normal'),
        ('hard', 'Hard'),
    )

    difficulty = models.CharField(max_length=6, choices=DIFFICULTY_CHOICES, default='medium')
    time_need = models.SmallIntegerField(null=True, blank=True)
    portions = models.SmallIntegerField(null=True, blank=True)

    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Recipe, self).save(*args, **kwargs)