from django import forms

from fieldwork.models import FieldData


class FieldDataForm(forms.ModelForm):

    class Meta:
        model = FieldData
        fields = [
            'title',
            'user',
            'brand_name',
            'pile_name',
            'slug',

            'merge_into_pile',
            'merge_with_pile',
            'new_pile_name',

            'image',
            'height_field',
            'width_field',
            'content',

            'turned',
            'watered',

            'humidity_measured_with',
            'core_humidity_readings',

            'temperature_measured_with',
            'core_temperature_readings',
            'celsius',

        ]
