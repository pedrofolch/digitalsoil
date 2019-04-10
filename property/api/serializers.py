from rest_framework import serializers

from assets.models import TypeOfAsset


class AssetSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

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

            # engines in engine_room
            # 'engine',

        ]
        read_only_fields = ['user', 'vin']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_vin(self, value):
        """We want the title to be unique"""
        qs = TypeOfAsset.objects.filter(vin__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(slug=self.instance.slug)
            if qs.exists():
                raise serializers.ValidationError("This VIN has already been used")
        return value
