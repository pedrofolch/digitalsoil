from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'url',
            'pk',
            'slug',
            'user',
            'title',
            'category',
            'sub_category',
            'price',
            'quantity',
            'pim',
            'in_stock',
            'active',
            'supplier',
            'image',
            'height_field',
            'width_field',
            'content',
            'draft',
            'publish',
            'read_time',
            'updated'
        ]

        read_only_fields = ['user']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_name(self, value):
        """We want the title to be unique"""
        qs = Product.objects.filter(name__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("This name has already been used")
        return value
