from rest_framework import serializers

from providers.models import Supplier, Supplies


class SupplierSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Supplier
        fields = [
            'url',
            'pk',
            "title",
            "contact",
            "content",
            "slug",
            "url",
            "user",
            "address",
            'merchant_category'
        ]
        read_only_fields = ['user']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_title(self, value):
        """We want the title to be unique"""
        qs = Supplier.objects.filter(title__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(slug=self.instance.slug)
            if qs.exists():
                raise serializers.ValidationError("This title has already been used")
        return value


class SuppliesSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Supplies
        fields = [
            'url',
            'pk',
            'customers'
        ]
        read_only_fields = ['user']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_title(self, value):
        """We want the title to be unique"""
        qs = Supplier.objects.filter(title__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(slug=self.instance.slug)
            if qs.exists():
                raise serializers.ValidationError("This Customer has already been used")
        return value


# class ZipCodeSerializer(serializers.ModelSerializer):
#     url = serializers.SerializerMethodField(read_only=True)
#
#     class Meta:
#         model = ZipCode
#         fields = [
#             'url',
#             'pk',
#             'code',
#             'poly'
#         ]
#         read_only_fields = ['user']

    # def get_url(self, obj):
    #     request = self.context.get('request')
    #     return obj.get_api_url(request=request)
    #
    # def validate_zipcode(self, value):
    #     """We want the title to be unique"""
    #     qs = ZipCode.objects.filter(code__iexact=value)  # including instance
    #     if self.instance:
    #         qs = qs.exclude(slug=self.instance.slug)
    #         if qs.exists():
    #             raise serializers.ValidationError("This title has already been used")
    #     return value


# class ElevationSerializer(serializers.ModelSerializer):
#     url = serializers.SerializerMethodField(read_only=True)
#
#     class Meta:
#         model = Elevation
#         fields = [
#             'url',
#             'pk',
#             'name',
#             'rast'
#         ]
#         read_only_fields = ['user']

    # def get_url(self, obj):
    #     request = self.context.get('request')
    #     return obj.get_api_url(request=request)
    #
    # def validate_elevation(self, value):
    #     """We want the title to be unique"""
    #     qs = Elevation.objects.filter(name__iexact=value)  # including instance
    #     if self.instance:
    #         qs = qs.exclude(slug=self.instance.slug)
    #         if qs.exists():
    #             raise serializers.ValidationError("This Name has already been used")
    #     return value
