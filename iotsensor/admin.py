from django.contrib import admin
from .models import SensorIoT, Headline, UserProfile

# Register your models here.


class SensorIoTModelAdmin(admin.ModelAdmin):
    list_display = ["title", "content", "timestamp"]
    list_display_links = ["content"]
    list_editable = ["title"]
    list_filter = ["title", "timestamp"]

    search_fields = ["title", "content"]

    class Meta:
        model = SensorIoT


admin.site.register(SensorIoT, SensorIoTModelAdmin)
admin.site.register(Headline)
admin.site.register(UserProfile)
