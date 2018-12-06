from django.contrib import admin


from recipes.models import Recipe, Tag

admin.site.register(Tag)
admin.site.register(Recipe)