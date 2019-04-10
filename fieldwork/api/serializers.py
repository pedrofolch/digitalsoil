from rest_framework import serializers

from fieldwork.models import FieldData


class FieldWorkSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FieldData
        fields = [
            'url',
            'title',
            'user',
            'brand_name',
            'pile_name',
            'slug',

            'merge_into_pile',
            'merge_with_pile',
            'new_pile_name',

            'image',
            'height_field',
            'width_field',
            'content',

            'turned',
            'watered',

            'humidity_measured_with',
            'core_humidity_readings',

            'temperature_measured_with',
            'core_temperature_readings',
            'celsius',

        ]
        read_only_fields = [
            'pk',
            'user'
        ]

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def get_owner(self, obj):
        request = self.context['request']
        if request.user.is_authenticated:
            if obj.user == request.user:
                return True
        return False
