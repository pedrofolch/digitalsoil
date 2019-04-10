from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Video, Category, TaggedItem
# Register your models here.


# admin.site.register(TaggedItem)

class TaggedItemInline(GenericTabularInline):
    model = TaggedItem


class VideoInline(admin.TabularInline):
    model = Video


class VideoAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline]
    list_display = ["__str__", 'slug']
    fields = ['title', 'order', 'share_message', 'embed_code', 'active', 'slug', 'featured', 'free_preview', 'category']
    prepopulated_fields = {'slug': ["title"], }

    class Meta:
        model = Video


admin.site.register(Video, VideoAdmin)


class CategoryAdmin(admin.ModelAdmin):
    inlines = [VideoInline, TaggedItemInline]

    class Meta:
        model = Category


admin.site.register(Category, CategoryAdmin)
