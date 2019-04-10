from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework import serializers

from fuel_station.models import FuelStation


User = get_user_model()


class UserPublicSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, allow_blank=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
        ]


class FuelStationSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api-fuel_station:detail',
        lookup_field='slug'
    )
    user = UserPublicSerializer(read_only=True)
    publish = serializers.DateField(default=timezone.now())
    owner = serializers.SerializerMethodField(read_only=True)

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

    def get_owner(self, obj):
        request = self.context['request']
        if request.user.is_authenticated:
            if obj.user == request.user:
                return True
        return False
