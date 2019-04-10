from django.contrib import admin
from .models import Product


class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated', 'category']
    list_display_link = ['in_stock']
    list_editable = ['title']
    list_filter = ['title', 'content']

    search_fields = ['title', 'content']

    class Meta:
        model = Product


admin.site.register(Product)
