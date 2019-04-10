from django.contrib import admin

from fieldwork.models import FieldData

#
# class InLineTemperature(admin.TabularInline):
#     model = Metric
#     extra = 3
#     max_num = 13
#
#
# class InLineHumidity(admin.TabularInline):
#     model = Humidity
#     extra = 3
#     max_num = 13
#
#
# class FieldDataAdmin(admin.ModelAdmin):
#     inlines = [InLineTemperature, InLineHumidity]
#     list_display = ('title',
#                     'user',
#                     'brand_name',
#                     'pile_name',
#                     'slug',
#
#                     'merge_into_pile',
#                     'merge_with_pile',
#                     'new_pile_name',
#
#                     'image',
#                     'height_field',
#                     'width_field',
#                     'content',
#
#                     'combine_title_and_slug'
#                     )
#     list_display_links = (
#         'title',
#         'combine_title_and_slug'
#     )
#
#     list_editable = ('slug',)
#
#     list_filter = ('title',
#                    'pile_name',
#                    'slug'
#                    )
#
#     search_fields = ('title',
#                      'pile_name',
#                      'brand_name',
#                      'slug'
#                      )
#
#     fieldsets = (
#         (None, {
#             'fields': (
#                 'title',
#                 'pile_name',
#                 'brand_name'
#
#             )
#         }),
#     )
#
#     def combine_title_and_slug(self, obj):
#         return "{} - {}".format(obj.title, obj.slug)
#
#
# admin.site.register(FieldData, FieldDataAdmin)

admin.site.register(FieldData)
