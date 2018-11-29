from django.contrib.auth.models import User
from django.db import models
from autoslug import AutoSlugField


class Tag(models.Model):
    name = models.CharField(max_length=63)
    slug = AutoSlugField(populate_from='name', unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=50)
    body = models.TextField()
    slug = AutoSlugField(populate_from='name', unique=True)
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