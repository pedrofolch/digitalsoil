from django import forms
from pagedown.widgets import PagedownWidget

from .models import Supplier  # , ZipCode, Elevation


class SupplierForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))
    publish = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Supplier
        fields = [
            "title",
            "contact",
            "content",
            "slug",
            "url",
            "user",
            "address",
            'merchant_category'
        ]


# class ZipCodeForm(forms.ModelForm):
#     content = forms.CharField(widget=PagedownWidget(show_preview=False))
#     publish = forms.DateField(widget=forms.SelectDateWidget)
#
#     class Meta:
#         model = ZipCode
#         fields =[
#             'code',
#             'poly'
#         ]
#
#
# class ElevationForm(forms.ModelForm):
#     content = forms.CharField(widget=PagedownWidget(show_preview=False))
#     publish = forms.DateField(widget=forms.SelectDateWidget)
#
#     class Meta:
#         model = Elevation
#         fields = [
#             'name',
#             'rast'
#         ]
