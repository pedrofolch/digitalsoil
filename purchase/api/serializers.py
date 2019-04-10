from rest_framework import serializers

from purchase.models import PurchaseOrder


class PurchaseSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = [
            'url',
            'pk',
            "title",
            "slug",
            'purchase_number',
            "supplier",
            "item",
            "product_number",
            "content",
            "quantity",
            "cost_of_item",
            "shipping_cost",
            "user",
            'for_asset',
            'for_engine',

        ]
        read_only_fields = ['user']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_purchase_number(self, value):
        """We want the purchase order number to be unique"""
        qs = PurchaseOrder.objects.filter(purchase_number__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(slug=self.instance.slug)
            if qs.exists():
                raise serializers.ValidationError("This Purchase Order Number has already been used")
        return value
