from django.contrib import admin
from .models import Lab

# Register your models here.


class LabModelAdmin(admin.ModelAdmin):
    list_display = ["title", "timestamp"]
    list_display_links = ["timestamp"]
    list_editable = ["title"]
    list_filter = ["title", "timestamp"]

    search_fields = ["title", "content"]

    class Meta:
        model = Lab


admin.site.register(Lab, LabModelAdmin)
