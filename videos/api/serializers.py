from rest_framework import serializers

from videos.models import Video


class VideoSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Video
        fields = [
            'uri',
            'pk',
            'title',
            'embed_code',
            'share_message',
            'order',
            'tags',
            'slug',
            'active',
            'featured',
            'free_preview',
            'category',
            'timestamp',
            'updated'
        ]
        read_only_fields = ['user', 'order', ]

    def get_uri(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_title(self, value):
        """We want the title to be unique"""
        qs = Video.objects.filter(title__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("This title has already been used")
        return value
