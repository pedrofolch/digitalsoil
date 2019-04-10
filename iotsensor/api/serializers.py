from rest_framework import serializers

from iotsensor.models import SensorIoT


class SensorIoTSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SensorIoT
        fields = [
            'url',
            'pk',
            'user',
            'title',
            'slug',
            'image',
            'height_field',
            'width_field',
            'content',
            'brand',
            'model',
            'year',
            'serial_number',
            'used_for',
            'color',
            'publish',
            'timestamp'
        ]
        read_only_fields = ['user']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_title(self, value):
        """We want the title to be unique"""
        qs = SensorIoT.objects.filter(title__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("This title has already been used")
        return value
