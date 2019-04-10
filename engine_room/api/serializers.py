from rest_framework import serializers

from engine_room.models import Engines, MainEngine, \
    CenterEngine, PortEngine, \
    PortEngine2, PortEngine3, \
    StarboardEngine, StarboardEngine2, \
    StarboardEngine3, Auxiliary, GenSet, GenSet2, Tools


class EnginesSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Engines
        fields = [
            'url',
            'pk',
            'user',
            'slug',
            'title',
            'main',
            'center',
            'port',
            'port2',
            'port3',
            'starboard',
            'starboard2',
            'starboard3',
            'auxiliary',
            'genset',
            'genset2',
            'tool_and_equipment',
            'engineer',
            'engine_on',
            'image',
            'height_field',
            'width_field',
            'content',

        ]
        read_only_fields = ['engine_model']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    # def validate_serial_number(self, value):
    #     """We want the title to be unique"""
    #     qs = Engines.objects.filter(serial_number__iexact=value)  # including instance
    #     if self.instance:
    #         qs = qs.exclude(slug=self.instance.slug)
    #         if qs.exists():
    #             raise serializers.ValidationError("This Signature Name has already been used")
    #     return value


class MainEngineSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MainEngine
        fields = [
            'ulr',
            'serial_number',
            'odometer',
            'miles',
            'kilometers',
            'engine_model',
            'year',
            'horsepower',
            'original',
            'number_of_cylinders',
            'fuel_type',
            'fuel_tank_capacity',
            'engine_oil_mark',
            'engine_oil_capacity',
            'image',
            'height_field',
            'width_field',
            'content',
            'engine_coolant_capacity',
            'engine_coolant_recommendation',
            'brake_fluid_recommendation',
            'automatic_trans_fluid_recommendation',
            'power_steering_fluid_recommendation',
            'differential_gear_oil_recommendation',
            'awd_mode_fluid_recommendation',
            'tire_size',
            'tire_pressure_front',
            'tire_pressure_rear'
        ]
        read_only_fields = ['user']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_serial_number(self, value):
        """We want the title to be unique"""
        qs = MainEngine.objects.filter(serial_number__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("This serial number has already been used")
        return value


class CenterEngineSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CenterEngine
        fields = [
            'ulr',
            'serial_number',
            'odometer',
            'in_hours',
            'engine_model',
            'original',
            'year',
            'horsepower',
            'outboard',
            'inboard',
            'number_of_cylinders',
            'fuel_type',
            'fuel_tank_capacity',
            'engine_oil_mark',
            'engine_oil_capacity',
            'image',
            'height_field',
            'width_field',
            'content'
        ]
        read_only_fields = ['user']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_serial_number(self, value):
        """We want the title to be unique"""
        qs = CenterEngine.objects.filter(serial_number__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("This serial number has already been used")
        return value


class PortEngineSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PortEngine
        fields = [
            'ulr',
            'serial_number',
            'in_hours',
            'engine_model',
            'original',
            'year',
            'horsepower',
            'outboard',
            'inboard',
            'number_of_cylinders',
            'fuel_type',
            'fuel_tank_capacity',
            'engine_oil_mark',
            'engine_oil_capacity',
            'image',
            'height_field',
            'width_field',
            'content'
        ]
        read_only_fields = ['user']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_serial_number(self, value):
        """We want the title to be unique"""
        qs = PortEngine.objects.filter(serial_number__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("This serial number has already been used")
        return value


class PortEngine2Serializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PortEngine2
        fields = [
            'ulr',
            'serial_number',
            'odometer',
            'in_hours',
            'engine_model',
            'original',
            'year',
            'horsepower',
            'outboard',
            'inboard',
            'number_of_cylinders',
            'fuel_type',
            'fuel_tank_capacity',
            'engine_oil_mark',
            'engine_oil_capacity',
            'image',
            'height_field',
            'width_field',
            'content'
        ]
        read_only_fields = ['user']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_serial_number(self, value):
        """We want the title to be unique"""
        qs = PortEngine2.objects.filter(serial_number__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("This serial number has already been used")
        return value


class PortEngine3Serializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PortEngine3
        fields = [
            'ulr',
            'serial_number',
            'odometer',
            'in_hours',
            'engine_model',
            'original',
            'year',
            'horsepower',
            'outboard',
            'inboard',
            'number_of_cylinders',
            'fuel_type',
            'fuel_tank_capacity',
            'engine_oil_mark',
            'engine_oil_capacity',
            'image',
            'height_field',
            'width_field',
            'content'
        ]
        read_only_fields = ['user']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_serial_number(self, value):
        """We want the title to be unique"""
        qs = PortEngine3.objects.filter(serial_number__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("This serial number has already been used")
        return value


class StarboardEngineSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StarboardEngine
        fields = [
            'ulr',
            'serial_number',
            'odometer',
            'in_hours',
            'engine_model',
            'original',
            'year',
            'horsepower',
            'outboard',
            'inboard',
            'number_of_cylinders',
            'fuel_type',
            'fuel_tank_capacity',
            'engine_oil_mark',
            'engine_oil_capacity',
            'image',
            'height_field',
            'width_field',
            'content'
        ]
        read_only_fields = ['user']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_serial_number(self, value):
        """We want the title to be unique"""
        qs = StarboardEngine.objects.filter(serial_number__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("This serial number has already been used")
        return value


class StarboardEngine2Serializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StarboardEngine2
        fields = [
            'ulr',
            'serial_number',
            'odometer',
            'in_hours',
            'engine_model',
            'original',
            'year',
            'horsepower',
            'outboard',
            'inboard',
            'number_of_cylinders',
            'fuel_type',
            'fuel_tank_capacity',
            'engine_oil_mark',
            'engine_oil_capacity',
            'image',
            'height_field',
            'width_field',
            'content'
        ]
        read_only_fields = ['user']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_serial_number(self, value):
        """We want the title to be unique"""
        qs = StarboardEngine2.objects.filter(serial_number__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("This serial number has already been used")
        return value


class StarboardEngine3Serializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StarboardEngine3
        fields = [
            'ulr',
            'serial_number',
            'odometer',
            'in_hours',
            'engine_model',
            'original',
            'year',
            'horsepower',
            'outboard',
            'inboard',
            'number_of_cylinders',
            'fuel_type',
            'fuel_tank_capacity',
            'engine_oil_mark',
            'engine_oil_capacity',
            'image',
            'height_field',
            'width_field',
            'content'
        ]
        read_only_fields = ['user']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_serial_number(self, value):
        """We want the title to be unique"""
        qs = StarboardEngine3.objects.filter(serial_number__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("This serial number has already been used")
        return value


class AuxiliaryEngineSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Auxiliary
        fields = [
            'ulr',
            'serial_number',
            'odometer',
            'in_hours',
            'engine_model',
            'original',
            'year',
            'horsepower',
            'outboard',
            'inboard',
            'number_of_cylinders',
            'fuel_type',
            'fuel_tank_capacity',
            'engine_oil_mark',
            'engine_oil_capacity',
            'image',
            'height_field',
            'width_field',
            'content'
        ]
        read_only_fields = ['user']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_serial_number(self, value):
        """We want the title to be unique"""
        qs = Auxiliary.objects.filter(serial_number__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("This serial number has already been used")
        return value


class GenSetSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = GenSet
        fields = [
            'ulr',
            'serial_number',
            'odometer',
            'in_hours',
            'engine_model',
            'original',
            'year',
            'horsepower',
            'portable',
            'number_of_cylinders',
            'fuel_type',
            'fuel_tank_capacity',
            'engine_oil_mark',
            'engine_oil_capacity',
            'image',
            'height_field',
            'width_field',
            'content'
        ]
        read_only_fields = ['user']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_serial_number(self, value):
        """We want the title to be unique"""
        qs = GenSet.objects.filter(serial_number__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("This serial number has already been used")
        return value


class GenSet2Serializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = GenSet2
        fields = [
            'ulr',
            'serial_number',
            'odometer',
            'in_hours',
            'engine_model',
            'original',
            'year',
            'horsepower',
            'portable',
            'number_of_cylinders',
            'fuel_type',
            'fuel_tank_capacity',
            'engine_oil_mark',
            'engine_oil_capacity',
            'image',
            'height_field',
            'width_field',
            'content'
        ]
        read_only_fields = ['user']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_serial_number(self, value):
        """We want the title to be unique"""
        qs = GenSet2.objects.filter(serial_number__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("This serial number has already been used")
        return value


class ToolsSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tools
        fields = [
            'ulr',
            'serial_number',
            'odometer',
            'in_hours',
            'engine_model',
            'original',
            'year',
            'horsepower',
            'number_of_cylinders',
            'fuel_type',
            'fuel_tank_capacity',
            'engine_oil_mark',
            'engine_oil_capacity',
            'image',
            'height_field',
            'width_field',
            'content'
        ]
        read_only_fields = ['user']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_serial_number(self, value):
        """We want the title to be unique"""
        qs = Tools.objects.filter(serial_number__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("This serial number has already been used")
        return value
