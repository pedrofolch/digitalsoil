from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework import serializers

from .models import TypeOfAsset


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


class AssetSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='assets-api:detail',
        lookup_field='slug'
    )
    user = UserPublicSerializer(read_only=True)
    publish = serializers.DateField(default=timezone.now())
    owner = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TypeOfAsset
        fields = [
            'url',
            'pk',
            'user',
            'title',
            'slug',

            'air_craft',
            'marine_vessel',
            'land_vehicle',
            'tool',

            'brand',
            'model',
            'year',
            'gross_weight',

            # visual of Asset
            'image',
            'height_field',
            'width_field',
            'content',

            # description of Asset
            'color',
            'vin',
            'license_plate',
            'used_for',
            'fuel',

            # if Draft = not finished do not publish
            'draft',

            # Certificate of Vehicle Registration
            'vehicle_classification',
            'license_plate',
            # 'audit_number',
            # 'd_g_v_w',
            'vin',
            'fees_paid',
            'wt_wheels',
            'body_type',
            'cylinders',

            'port_of_registry',
            'reg_exp_date',

            'registered_owner',
            'owners_address',

            'is_it_insured',
            'insurance_provider',
            'insurance_type',
            'insurance_cost',
            'insurance_policy_number',
            # 'starting_policy_date',
            # 'ending_policy_date',
            'emergency_roadside_assistance',
            'assistance_miles',

            # Exterior Dimensions
            'wheelbase',
            'overall_length',
            'overall_height',
            'min_ground_clearance',
            'base_curb_weight',

            # Wheels
            'front_wheel_diameter',
            'rear_wheel_diameter',

            'wheel_rims_type',
            'wheel_rims_model',

            # Tires
            'front_tire_type',
            'rear_tire_type',
            'original_msrp',
            'price_paid',

            # engines
            # 'engine',
        ]

    def get_owner(self, obj):
        request = self.context['request']
        if request.user.is_authenticated:
            if obj.user == request.user:
                return True
        return False
