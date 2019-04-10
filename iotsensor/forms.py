from django import forms
from pagedown.widgets import PagedownWidget

from .models import SensorIoT


class SensorIoTForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=True))
    publish = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = SensorIoT
        fields = [
            'user',
            'title',
            'slug',
            'url',
            'image',
            'height_field',
            'width_field',
            'content',
            'brand',
            'model',
            'year',
            'serial_number',
            'used_for',
            'color'
        ]
