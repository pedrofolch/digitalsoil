from django import forms
from pagedown.widgets import PagedownWidget

from .models import Product


class ProductForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=True))
    publish = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Product
        fields = [
            "user",
            "title",
            "category",
            "sub_category",
            "price",
            'quantity',
            'pim',
            'in_stock',
            'active',
            'supplier',
            "slug",
            "image",
            "height_field",
            "width_field",
            "content",
            "draft",
            "publish",
            "read_time"
        ]
