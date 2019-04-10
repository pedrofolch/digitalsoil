from rest_framework import serializers

from fuel_station.models import FuelStation


class FuelStationSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FuelStation
        fields = [
            'url',
            'pk',
            'user',

            'title',
            'slug',

            'vehicle',
            'invoice_number',
            'date',

            'fuel_type_pumped',
            'price_per_gal',
            'amount_of_fuel',
            'fuel_total',

            'current_miles',

            'fueled_by',
            'draft',

            # image
            'image',
            'height_field',
            'width_field',
            'content',
        ]
        read_only_fields = ['user']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_serial_number(self, value):
        """We want the title to be unique"""
        qs = FuelStation.objects.filter(invoice_number__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(slug=self.instance.slug)
            if qs.exists():
                raise serializers.ValidationError("This Signature Name has already been used")
        return value
