from rest_framework import serializers

from posts.models import Post


class BlogPostSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            'url',
            'pk',

            "blog",
            'title',
            'slug',
            'headline',
            'user',
            "image",
            'height_field',
            'width_field',
            "content",

            "draft",
            'read_time',
            'authors',
            'rating'
        ]
        read_only_fields = ['user']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_headline(self, value):
        """We want the title to be unique"""
        qs = Post.objects.filter(headline__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("This headline has already been used")
        return value
