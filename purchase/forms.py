from django import forms
from pagedown.widgets import PagedownWidget

from .models import PurchaseOrder


class PurchaseOrderForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))

    class Meta:
        model = PurchaseOrder
        fields = [
            "title",
            "slug",
            'purchase_number',

            "supplier",
            "item",
            'product_number',
            "content",
            'quantity',

            "cost_of_item",
            "shipping_cost",

            "user",
            'for_asset',
            'for_engine',
        ]
