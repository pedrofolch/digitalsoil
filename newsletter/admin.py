from django.contrib import admin

from newsletter.models import SignUp, Newsletter


# Register your models here.
class SignUpAdmin(admin.ModelAdmin):
    list_display = ["__str__", "timestamp", "updated"]


admin.site.register(SignUp, SignUpAdmin)
admin.site.register(Newsletter)
