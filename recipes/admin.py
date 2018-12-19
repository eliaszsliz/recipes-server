from django.contrib import admin


from recipes.models import Recipe, Tag
from imagekit.admin import AdminThumbnail

class TagAdmin(admin.ModelAdmin):
    list_display = ('admin_thumbnail', '__str__', )
    exclude = ('slug', )
    admin_thumbnail = AdminThumbnail(image_field='image_thumbnail')
    list_display_links = ('admin_thumbnail', '__str__')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('admin_thumbnail', '__str__', )
    exclude = ('slug', )
    admin_thumbnail = AdminThumbnail(image_field='image_thumbnail')
    list_display_links = ('admin_thumbnail', '__str__')


admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)