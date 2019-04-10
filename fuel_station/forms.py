from django import forms
from pagedown.widgets import PagedownWidget

from .models import FuelStation


class FuelStationForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=True))
    publish = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = FuelStation
        fields = [
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
