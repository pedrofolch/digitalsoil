from rest_framework import serializers

from assets.models import MarineVessel, Automobile, TypeOfAsset, Equipment, Parts, \
    Asset, CarManufacturer, MarineVesselManufacturer, EquipmentManufacturer, \
    CarModelType, MarineModelType, EquipmentModelType, ThroughHull, HeavyEquipmentManufacturer, HeavyEquipmentModelType


class TypeOfAssetSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TypeOfAsset
        fields = [
            'url',
            'pk',
            'user',
            'title',
            'slug',
            'user',
            'asset',

            'image',
            'height_field',
            'width_field',
            'content',

            # asset type
            'marine_vessel',
            'land_vehicle',
            'tool',

            'draft',
            'location_of_asset'
        ]
        read_only_fields = ['user', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)


class MarineVesselSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MarineVessel
        fields = [
            'url',
            'pk',
            'user',
            'title',
            'slug',

            'port_of_registry',
            'reg_exp_date',
            'vehicle_classification',

            'brand',
            'model',
            'year',
            'gross_weight',
            'hull_number',
            'hull_type',
            'hull_material',

            'number_of_through_holes',

            # visual of Asset
            'image',
            'height_field',
            'width_field',
            'content',
            'used_for',

            # Registered to
            'registered_owner',
            'owners_address',

            # insurance policy
            'is_it_insured',
            'insurance_provider',
            'insurance_type',
            'insurance_cost',
            'insurance_policy_number',
            'seatow',
            'assistance_miles',

            # Original MSRP
            'original_msrp',
            'price_paid',

            # Vessel Dimension
            'reported_loa',
            'reported_lwl',
            'reported_beam',
            'reported_draft',
            'max_height'

        ]
        read_only_fields = ['user', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_hull_number(self, value):
        """We want the title to be unique"""
        qs = MarineVessel.objects.filter(hull_number__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(slug=self.instance.slug)
            if qs.exists():
                raise serializers.ValidationError("This Hull No. has already been used")
        return value


class AutomobileSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Automobile
        fields = [
            'url',
            'pk',
            'user',
            'title',
            'slug',

            'brand',
            'model',
            'year',
            'gross_weight',

            # visual of Asset
            'image',
            'height_field',
            'width_field',
            'content',

            # description of asset
            'used_for',
            'color',
            'fuel',
            'license_plate',
            'vin',
            'fees_paid',
            'wt_wheels',
            'body_type',
            'cylinders',

            # Registered to
            'registered_owner',
            'owners_address',

            # insurance policy
            'is_it_insured',
            'insurance_provider',
            'insurance_type',
            'insurance_cost',
            'insurance_policy_number',
            'emergency_roadside_assistance',
            'assistance_miles',

            # vehicle Exterior Dimensions
            'wheelbase',
            'overall_length',
            'overall_height',
            'min_ground_clearance',
            'base_curb_weight'
        ]
        read_only_fields = ['user', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_vin(self, value):
        """We want the title to be unique"""
        qs = Automobile.objects.filter(vin__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(slug=self.instance.slug)
            if qs.exists():
                raise serializers.ValidationError("This Hull No. has already been used")
        return value

    def validate_license_plate(self, value):
        """We want the title to be unique"""
        qs = Automobile.objects.filter(license_plate__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(slug=self.instance.slug)
            if qs.exists():
                raise serializers.ValidationError("This license plate. has already been used")
        return value


class EquipmentAssetSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TypeOfAsset
        fields = [
            'url',
            'pk',
            'title',
            'slug',
            'user',

            'brand',
            'model',
            'year',
            'gross_weight',

            # visual of Asset
            'image',
            'height_field',
            'width_field',
            'content',

            # description of asset
            'used_for',
            'color',
            'fuel',
            'usage_meter'
        ]
        read_only_fields = ['user', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_serial(self, value):
        """We want the title to be unique"""
        qs = Equipment.objects.filter(serial__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(slug=self.instance.slug)
            if qs.exists():
                raise serializers.ValidationError("This serial number has already been used")
        return value


class PartsSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Parts
        fields = [
            'url',
            'pk',
            'title',
            'part_number',

            'image',
            'height_field',
            'width_field',
            'content',
            'used_for',
            'price'
        ]
        read_only_fields = ['pk', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_part_number(self, value):
        """We want the title to be unique"""
        qs = Parts.objects.filter(part_number__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(slug=self.instance.slug)
            if qs.exists():
                raise serializers.ValidationError("This Part No. has already been used")
        return value


class AssetSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Asset
        fields = [
            'url',
            'pk',
            'user',
            'serial_number',
            'odometer',
            'in_miles',
            'in_kilometers',
            'in_hours'
        ]
        read_only_fields = ['pk', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_serial_number(self, value):
        """We want the title to be unique"""
        qs = Asset.objects.filter(serial_number__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(slug=self.instance.slug)
            if qs.exists():
                raise serializers.ValidationError("This Serial No. has already been used")
        return value


class CarManufacturerSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CarManufacturer
        fields = [
            'url',
            'pk',
            'title',

        ]
        read_only_fields = ['pk', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)


class HeavyEquipmentManufacturerSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = HeavyEquipmentManufacturer
        fields = [
            'url',
            'pk',
            'title',

        ]
        read_only_fields = ['pk', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)


class MarineVesselManufacturerSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MarineVesselManufacturer
        fields = [
            'url',
            'pk',
            'title'

        ]
        read_only_fields = ['pk', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_title(self, value):
        """We want the title to be unique"""
        qs = MarineVesselManufacturer.objects.filter(title__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(slug=self.instance.slug)
            if qs.exists():
                raise serializers.ValidationError("This Brand has already exist")
        return value


class EquipmentManufacturerSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = EquipmentManufacturer
        fields = [
            'url',
            'pk',
            'title'
        ]
        read_only_fields = ['pk', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_title(self, value):
        """We want the title to be unique"""
        qs = EquipmentManufacturer.objects.filter(title__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(slug=self.instance.slug)
            if qs.exists():
                raise serializers.ValidationError("This Brand has already exist")
        return value


class CarModelTypeSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CarModelType
        fields = [
            'url',
            'pk',
            'title'
        ]
        read_only_fields = ['pk', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)


class HeavyEquipmentModelTypeSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = HeavyEquipmentModelType
        fields = [
            'url',
            'pk',
            'title'
        ]
        read_only_fields = ['pk', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)


class MarineModelTypeSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MarineModelType
        fields = [
            'url',
            'pk',
            'title'
        ]
        read_only_fields = ['pk', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)


class EquipmentModelTypeSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = EquipmentModelType
        fields = [
            'url',
            'pk',
            'title'
        ]
        read_only_fields = ['pk', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)


class ThroughHullSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ThroughHull
        fields = [
            'url',
            'pk',
            'title',
            'part'
        ]
        read_only_fields = ['pk', 'url', 'part', 'title']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)
