from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from graphql.error import GraphQLLocatedError
from tinymce.models import HTMLField

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust, SmartResize, Thumbnail, ResizeToFit

import logging
logger = logging.getLogger(__name__)


class GrapheneFieldsMixin:
    def background_url(self):
        try:
            image = self.image_top
            if not image:
                image.generate()
            return self.image_top.url
        except FileNotFoundError:
            logger.warning('File: %s is missing and will be removed from database ' % self.image.name)
            return None

    def thumbnail_url(self):
        try:
            image = self.image_thumbnail
            if not image:
                image.generate()
            return self.image_thumbnail.url
        except FileNotFoundError:
            logger.warning('File: %s is missing and will be removed from database ' % self.image.name)
            return None


class Tag(GrapheneFieldsMixin, models.Model):
    name = models.CharField(max_length=63)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = HTMLField(blank=True, null=True)

    image = models.ImageField(blank=True, null=True, upload_to='images')
    image_top = ImageSpecField(source='image',
                               processors=[
                                   SmartResize(1000, 400)
                               ],
                               format='JPEG',
                               options={'quality': 60})

    image_thumbnail = ImageSpecField(source='image',
                                     processors=[
                                         Thumbnail(64, 64),
                                         Adjust(sharpness=1.2)
                                     ],
                                     format='JPEG',
                                     options={'quality': 100})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)


class Recipe(GrapheneFieldsMixin, models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, null=True)

    image = models.ImageField(blank=True, null=True, upload_to='images')
    image_top = ImageSpecField(source='image',
                               processors=[
                                   SmartResize(1000, 400)
                               ],
                               format='JPEG',
                               options={'quality': 60})

    image_thumbnail = ImageSpecField(source='image',
                                     processors=[
                                         ResizeToFit(330, 220),
                                         Adjust(sharpness=1.1)
                                     ],
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

    def set_favourite(self, user, state_to_set):
        if not state_to_set:
            current_state = self.favourites.filter(pk=user.pk).exists()
            state_to_set = not current_state

        if state_to_set:
            self.favourites.add(user)
        else:
            self.favourites.remove(user)

        return True
