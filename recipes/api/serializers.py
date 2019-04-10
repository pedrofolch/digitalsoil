from rest_framework import serializers

from recipes.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'url',
            'pk',
            'producer',
            'pile_name',
            'slug',
            'content',
            'draft',
            'observation',
            'pub_date',
            'user',
            'ready_to_use',
            'public',
            'category',
            'category_value',
            'recipe_name',
            'nitrogen_material',
            'type_of_bucket_nitrogen',
            'amount_nitrogen',
            'nitrogen_material_two',
            'type_of_bucket_nitrogen_two',
            'amount_nitrogen_two',
            'nitrogen_material_three',
            'type_of_bucket_nitrogen_three',
            'amount_nitrogen_three',
            'high_nitrogen_material',
            'type_of_bucket_high_nitrogen',
            'amount_high_nitrogen',
            'high_nitrogen_material_two',
            'type_of_bucket_high_nitrogen_two',
            'amount_high_nitrogen_two',
            'high_nitrogen_material_three',
            'type_of_bucket_high_nitrogen_three',
            'amount_high_nitrogen_three',
            'carbon_material',
            'type_of_bucket_carbon',
            'amount_carbon',
            'carbon_material_two',
            'type_of_bucket_carbon_two',
            'amount_carbon_two',
            'carbon_material_three',
            'type_of_bucket_carbon_three',
            'amount_carbon_three',
            'wide',
            'length',
            'tall'
        ]
        read_only_fields = ['user']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_title(self, value):
        """We want the title to be unique"""
        qs = Recipe.objects.filter(title__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(slug=self.instance.slug)
            if qs.exists():
                raise serializers.ValidationError("This Signature Name has already been used")
        return value
