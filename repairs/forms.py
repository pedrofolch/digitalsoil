from django import forms
from pagedown.widgets import PagedownWidget

from .models import RepairFile, RepairOrder


class RepairForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=True))
    date_of_invoice = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = RepairFile
        fields = [
            'user',

            'title',
            'slug',
            'service_provider',
            'date_of_invoice',


            'estimate_number',
            'quoted_price',

            'invoice_number',
            'work_order',
            'odometer',
            'tax_id',
            'return_parts',
            'due_price',
            'price_paid',
            'asset',
            'engine',


            'part_no',
            'quantity',
            'unit_price',
            'total',

            # image
            'image',
            'height_field',
            'width_field',
            'content',
        ]


class RepairOrderForm(forms.ModelForm):
    problem_found = forms.CharField(widget=PagedownWidget(show_preview=True))
    publish = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = RepairOrder
        fields = [
            'user',

            'title',
            'slug',
            'purchase_order',
            'estimate',
            'po_number',
            'on_asset',
            'problem_found',
            'approved',
            'approved_by',
            'assigned_to',
            'preferred_engineer'
        ]
