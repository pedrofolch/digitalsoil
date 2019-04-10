from django import forms
from pagedown.widgets import PagedownWidget

from .models import MarineVessel, Automobile, TypeOfAsset, Equipment, \
    Parts, CarManufacturer, MarineVesselManufacturer, EquipmentManufacturer, \
    CarModelType, MarineModelType, EquipmentModelType, ThroughHull, Asset, HeavyEquipmentManufacturer, \
    HeavyEquipmentModelType


class MarineAssetForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=True))

    class Meta:
        model = MarineVessel
        fields = [
            'user',
            'title',
            'slug',
            'user',

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


class AutomobileAssetForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=True))

    class Meta:
        model = Automobile
        fields = [
            'user',
            'title',
            'slug',
            'engineering_equipment',
            'user',

            'brand',
            'model',
            'year',
            'gross_weight',
            # 'odometer',

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


class EquipmentAssetForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=True))

    class Meta:
        model = Equipment
        fields = [
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
            'fuel'
        ]


class TypeOfAssetForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=True))

    class Meta:
        model = TypeOfAsset
        fields = [
            'title',
            'slug',

            # asset type

            'marine_vessel',
            'land_vehicle',
            'tool',

            'draft',
            'location_of_asset',
            'image',
            'height_field',
            'width_field',
            'content',
            'user'

        ]


class PartsForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=True))

    class Meta:
        model = Parts
        fields = [
            'title',
            'part_number',

            'image',
            'height_field',
            'width_field',
            'content',
            'used_for',
            'price'
        ]


class AssetForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=True))

    class Meta:
        model = Asset
        fields = [
            'serial_number',
            'user',
            'odometer',
            'in_miles',
            'in_kilometers',
            'in_hours'
        ]


class CarManufacturerForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=True))

    class Meta:
        model = CarManufacturer
        fields = [
            'title'
        ]


class HeavyEquipmentManufacturerForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=True))

    class Meta:
        model = HeavyEquipmentManufacturer
        fields = [
            'title'
        ]


class HeavyEquipmentModelTypeForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=True))

    class Meta:
        model = HeavyEquipmentModelType
        fields = [
            'title'
        ]


class MarineVesselManufacturerForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=True))

    class Meta:
        model = MarineVesselManufacturer
        fields = [
            'title'
        ]


class EquipmentManufacturerForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=True))

    class Meta:
        model = EquipmentManufacturer
        fields = [
            'title'
        ]


class CarModelTypeForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=True))

    class Meta:
        model = CarModelType
        fields = [
            'title'
        ]


class MarineModelTypeForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=True))

    class Meta:
        model = MarineModelType
        fields = [
            'title'
        ]


class EquipmentModelTypeForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=True))

    class Meta:
        model = EquipmentModelType
        fields = [
            'title'
        ]


class ThroughHullForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=True))

    class Meta:
        model = ThroughHull
        fields = [
            'title',
            'part'
        ]
