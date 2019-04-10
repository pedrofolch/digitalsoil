from rest_framework import serializers

from repairs.models import RepairFile, RepairOrder


class RepairSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RepairFile
        fields = [
            'url',
            'pk',
            'user',

            'title',
            'slug',
            'service_provider',
            'date_of_invoice',

            'estimate_number',
            'quoted_price',

            'invoice_number',
            'work_order',
            'odometer',
            'tax_id',
            'return_parts',
            'due_price',
            'price_paid',
            'asset',
            'engine',

            'part_no',
            'quantity',
            'unit_price',
            'total',

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
        qs = RepairFile.objects.filter(invoice_number__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(slug=self.instance.slug)
            if qs.exists():
                raise serializers.ValidationError("This Signature Name has already been used")
        return value


class RepairOrderSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RepairOrder
        fields = [
            'url',
            'pk',
            'slug',
            'user',
            'title',
            'purchase_order',
            'estimate',
            'po_number',
            'on_asset',
            'problem_found',
            'date_reported',
            'approved',
            'approved_by',
            'assigned_to',
            'preferred_engineer'
        ]
        read_only_fields = ['user']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_po_number(self, value):
        """We want the title to be unique"""
        qs = RepairOrder.objects.filter(po_number__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(slug=self.instance.slug)
            if qs.exists():
                raise serializers.ValidationError("This Number has already been used")
        return value
