from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from graphql.error import GraphQLLocatedError
from tinymce.models import HTMLField

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from imagekit.processors import SmartResize


class Tag(models.Model):
    name = models.CharField(max_length=63)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = HTMLField(blank=True, null=True)

    image = models.ImageField(blank=True, null=True, upload_to='images')
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(50, 50)],
                                     format='JPEG',
                                     options={'quality': 60})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)


class Recipe(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, null=True)

    image = models.ImageField(blank=True, null=True, upload_to='images')
    image_top = ImageSpecField(source='image',
                               processors=[ResizeToFill(1000, 400)],
                               format='JPEG',
                               options={'quality': 60})

    image_thumbnail = ImageSpecField(source='image',
                                     processors=[SmartResize(300, 200)],
                                     format='JPEG',
                                     options={'quality': 60})

    body = HTMLField()
    tags = models.ManyToManyField(Tag, related_name='recipes', blank=True)
    favourites = models.ManyToManyField(User, related_name='favoured', blank=True)

    DIFFICULTY_CHOICES = (
        ('easy', 'Easy'),
        ('medium', 'Normal'),
        ('hard', 'Hard'),
    )

    difficulty = models.CharField(max_length=6,
                                  choices=DIFFICULTY_CHOICES,
                                  default='medium',
                                  blank=True, null=True)
    time_need = models.SmallIntegerField(null=True, blank=True)
    portions = models.SmallIntegerField(null=True, blank=True)

    description = HTMLField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Recipe, self).save(*args, **kwargs)

    def thumbnail_url(self):
        return self.image_thumbnail.url

    def background_url(self):
        return self.image_top.url
