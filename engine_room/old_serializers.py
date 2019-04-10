from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework import serializers

from engine_room.models import Engines


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


class EnginesSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='engine-api:detail',
        lookup_field='slug'
    )
    user = UserPublicSerializer(read_only=True)
    publish = serializers.DateField(default=timezone.now())
    owner = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Engines
        fields = [
            'url',
            'pk',
            'user',
            'slug',
            'title',
            'engine_model',
            'year',
            'horsepower',
            'serial_number',
            'engine_side',
            'engine_on',
            'odometer',
            # 'in_miles',
            # 'in_kilometers',
            # 'in_hours',
            'image',
            'height_field',
            'width_field',
            'content',
            'number_of_cylinders',
            'fuel_type',
            'fuel_tank_capacity',
            'engine_oil_mark',
            'engine_oil_capacity',
            'engine_coolant_recommendation',
            'engine_coolant_capacity',
            'brake_fluid_recommendation',
            'automatic_trans_fluid_recommendation',
            'power_steering_fluid_recommendation',
            'awd_mode_fluid_recommendation',
            'tire_pressure_front',
            'tire_pressure_rear',
            'need_repairs'
        ]

    def get_owner(self, obj):
        request = self.context['request']
        if request.user.is_authenticated:
            if obj.user == request.user:
                return True
        return False
