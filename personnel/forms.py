from django import forms
from pagedown.widgets import PagedownWidget

from .models import MarineVessel, Automobile


class MarineAssetForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=True))

    class Meta:
        model = MarineVessel
        fields = [
            'user',
            'title',
            'slug',
            'hull_no',

            'port_of_registry',
            'reg_exp_date',
            'vehicle_classification',

            'brand',
            'model',
            'year',
            'gross_weight',

            # odometers
            'center_engine',
            'port_engine',
            'port_engine2',
            'port_engine3',
            'starboard_engine',
            'starboard_engine2',
            'starboard_engine3',
            'auxiliary_engine',
            'genset',
            'genset2',

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
            'seaTow',
            'assistance_miles',

            # Original MSRP
            'original_msrp',
            'price_paid',

            # Vessel Dimension
            'reported_loa',
            'reported_lwl',
            'reported_beam',
            'reported_draft',
            'max_height',

        ]


class AutomobileAssetForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=True))

    class Meta:
        model = Automobile
        fields = [
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


class TypeOfAsset(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=True))

    class Meta:
        model = TypeOfAsset
        fields = [
            'user',
            'title',
            'slug',

            # asset type
            'air_craft',
            'marine_vessel',
            'land_vehicle',
            ''

        ]