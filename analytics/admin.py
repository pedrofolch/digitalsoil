from django.contrib import admin

# Register your models here.

from .models import PageView

from import_export.admin import ImportExportModelAdmin
from .models import View


@admin.register(View)
class ViewAdmin(ImportExportModelAdmin):
    pass


admin.site.register(PageView)