from django import forms
from pagedown.widgets import PagedownWidget

from .models import Engines, MainEngine, \
    CenterEngine, PortEngine, \
    PortEngine2, PortEngine3, \
    StarboardEngine, StarboardEngine2, \
    StarboardEngine3, Auxiliary, GenSet, GenSet2, Tools


class EnginesForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=True))
    publish = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Engines
        fields = [
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


class MainEngineForm(forms.Form):
    serial_number = forms.CharField()
    miles = forms.BooleanField()
    kilometers = forms.BooleanField()
    engine_model = forms.CharField()
    year = forms.CharField()
    horsepower = forms.IntegerField()
    original = forms.BooleanField()
    number_of_cylinders = forms.IntegerField()
    fuel_type = forms.CharField()
    fuel_tank_capacity = forms.DecimalField()
    engine_oil_mark = forms.CharField()
    engine_oil_capacity = forms.DecimalField()
    image = forms.ImageField()
    height_field = forms.IntegerField()
    width_field = forms.IntegerField()
    content = forms.CharField(widget=PagedownWidget(show_preview=False))
    engine_coolant_recommendation = forms.CharField()
    engine_coolant_capacity = forms.DecimalField()
    brake_fluid_recommendation = forms.CharField()
    automatic_trans_fluid_recommendation = forms.CharField(max_length=100)
    power_steering_fluid_recommendation = forms.CharField(max_length=100)
    differential_gear_oil_recommendation = forms.CharField(max_length=100)
    awd_mode_fluid_recommendation = forms.CharField(max_length=100)
    tire_size = forms.CharField(max_length=11)
    tire_pressure_front = forms.IntegerField()
    tire_pressure_rear = forms.IntegerField()

    class Meta:
        model = MainEngine
        fields = [
            'serial_number',
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


class CenterEngineForm(forms.Form):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))

    class Meta:
        model = CenterEngine
        fields = [
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


class PortEngineForm(forms.Form):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))

    class Meta:
        model = PortEngine
        fields = [
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


class PortEngine2Form(forms.Form):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))

    class Meta:
        model = PortEngine2
        fields = [
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


class PortEngine3Form(forms.Form):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))

    class Meta:
        model = PortEngine3
        fields = [
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


class StarboardEngineForm(forms.Form):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))

    class Meta:
        model = StarboardEngine
        fields = [
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


class StarboardEngine2Form(forms.Form):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))

    class Meta:
        model = StarboardEngine2
        fields = [
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


class StarboardEngine3Form(forms.Form):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))

    class Meta:
        model = StarboardEngine3
        fields = [
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


class AuxiliaryEngineForm(forms.Form):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))

    class Meta:
        model = Auxiliary
        fields = [
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


class GenSetForm(forms.Form):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))

    class Meta:
        model = GenSet
        fields = [
            'serial_number',
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


class GenSet2Form(forms.Form):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))

    class Meta:
        model = GenSet2
        fields = [
            'serial_number',
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


class ToolsForm(forms.Form):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))

    class Meta:
        model = Tools
        fields = [
            'serial_number',
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
