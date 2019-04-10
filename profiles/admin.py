from django.contrib import admin

from .models import Profile, Address


class ProfileAdmin(admin.ModelAdmin):

    class Meta:
        model = Profile


admin.site.register(Profile, ProfileAdmin)


class AddressAdmin(admin.ModelAdmin):

    class Meta:
        model = Address


admin.site.register(Address, AddressAdmin)

# admin.site.register(Profile)
# admin.site.register(Address)
