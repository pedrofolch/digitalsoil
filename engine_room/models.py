from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.urls import reverse
# from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from rest_framework.reverse import reverse as api_reverse

from comments.models import Comment
from markdown_deux import markdown
from .utils import get_read_time
from assets.models import TypeOfAsset
from personnel.models import Engineer
User = settings.AUTH_USER_MODEL
from assets.models import Asset

# Create your models here.


ASSET_CHOICES = (
    ('T', 'tool'),
    ('U', 'uninspected passenger vessel'),
    ('P', 'personal water craft'),
    ('R', 'rv'),
    ('C', 'car'),
    ('S', 'SUV'),
    ('Tr', 'truck'),
    ('H', 'heavy equipment'),
    ('A', 'air craft vessel'),
)

FUEL_TYPE_CHOICES = (
    ('86', 'Gasoline-86'),
    ('89', 'Gasoline-89'),
    ('90', 'Gasoline-90'),
    ('D', 'Diesel'),
    ('FF', 'Flex fuel'),
    ('E', 'Electric'),
    ('EG', 'Hybrid'),
    ('S', 'Solar'),
    ('H', 'Hydrogen'),
    ('2C', 'Two Cycle fuels')
)

FUEL_CHOICES = (
    ('G', 'gasoline'),
    ('D', 'diesel'),
    ('M', 'mix two cycle'),
    ('E', 'electric'),
    ('H', 'hybrid'),
    ('W', 'wind'),
    ('P', 'human powered'),
)

YEAR_CHOICES = (
    ('2019', '2019'),
    ('2018', '2018'),
    ('2017', '2017'),
    ('2016', '2016'),
    ('2015', '2015'),
    ('2014', '2014'),
    ('2013', '2013'),
    ('2012', '2012'),
    ('2011', '2011'),
    ('2010', '2010'),
    ('2009', '2009'),
    ('2008', '2008'),
    ('2007', '2007'),
    ('2006', '2006'),
    ('2005', '2005'),
    ('2004', '2004'),
    ('2003', '2003'),
    ('2002', '2002'),
    ('2001', '2001'),
    ('1999', '1999'),
    ('1998', '1998'),
    ('1997', '1997'),
    ('1996', '1996'),
    ('1995', '1995'),
    ('1994', '1994'),
    ('1993', '1993'),
    ('1992', '1992'),
    ('1991', '1991'),
    ('1990', '1990'),
    ('1989', '1989'),
    ('1988', '1988'),
    ('1987', '1987'),
    ('1986', '1986'),
    ('1985', '1985'),
    ('1984', '1984'),
    ('1983', '1983'),
)

ENGINE_MODEL_CHOICE = (
    ('IN', 'infiniti'),
    ('HO', 'honda'),
    ('TO', 'toyota'),
    ('MZ', 'mazda'),
    ('BM', 'bmw'),
    ('MB', 'mercedez benz'),
    ('FD', 'ford'),
    ('CV', 'chevy'),
    ('GM', 'general motors'),
    ('ST', 'saturn'),
    ('CH', 'christler'),
    ('JP', 'Jeep'),
    ('AU', 'audi')
)


def upload_port_engine_location(instance, filename):
    engine_models = instance.__class__
    new_id = engine_models.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


def upload_port_engine2_location(instance, filename):
    engine_models = instance.__class__
    new_id = engine_models.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


def upload_port_engine3_location(instance, filename):
    engine_models = instance.__class__
    new_id = engine_models.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


def upload_starboard_engine_location(instance, filename):
    engine_models = instance.__class__
    new_id = engine_models.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


def upload_starboard_engine2_location(instance, filename):
    engine_models = instance.__class__
    new_id = engine_models.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


def upload_starboard_engine3_location(instance, filename):
    engine_models = instance.__class__
    new_id = engine_models.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


def upload_center_engine_location(instance, filename):
    engine_models = instance.__class__
    new_id = engine_models.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


def upload_main_engine_location(instance, filename):
    engine_models = instance.__class__
    new_id = engine_models.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


def upload_engine_location(instance, filename):
    engine_models = instance.__class__
    new_id = engine_models.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


def upload_tool_location(instance, filename):
    engine_models = instance.__class__
    new_id = engine_models.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


def upload_auxiliary_location(instance, filename):
    engine_models = instance.__class__
    new_id = engine_models.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


def upload_genset_location(instance, filename):
    engine_models = instance.__class__
    new_id = engine_models.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


def upload_genset2_location(instance, filename):
    engine_models = instance.__class__
    new_id = engine_models.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


def upload_engine_room_location(instance, filename):
    engine_models = instance.__class__
    new_id = engine_models.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object,
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


# Odometers
class MainEngine(models.Model):
    # defines Car or land vehicle engine
    serial_number = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True)
    miles = models.BooleanField(default=True)
    kilometers = models.BooleanField(default=False)
    engine_model = models.CharField(max_length=122, null=True, blank=True)
    year = models.CharField(max_length=4, choices=YEAR_CHOICES, default='1999')
    horsepower = models.PositiveIntegerField(default=0)
    original = models.BooleanField(default=True)
    number_of_cylinders = models.IntegerField(default=4)
    fuel_type = models.CharField(max_length=2, choices=FUEL_TYPE_CHOICES, default='89')
    fuel_tank_capacity = models.DecimalField(max_digits=6, decimal_places=2, default='21.13')
    engine_oil_mark = models.CharField(max_length=20, default='mark SAE 5W-30')
    engine_oil_capacity = models.DecimalField(decimal_places=2, max_digits=6, default=3.88, help_text='in quarts')

    # visual of engine
    image = models.ImageField(upload_to=upload_main_engine_location, null=True, blank=True, width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField('Description/Conditions/Note', blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    # quick reference
    engine_coolant_recommendation = models.CharField(max_length=30, default='Antifreeze coolant',
                                                     blank=True, null=True)
    engine_coolant_capacity = models.DecimalField(max_digits=4, decimal_places=2, default=11.25, help_text='in quarts',
                                                  blank=True, null=True)
    brake_fluid_recommendation = models.CharField(max_length=20, default='DOT 3', blank=True, null=True)
    automatic_trans_fluid_recommendation = models.CharField(max_length=100,
                                                            default='Nissan Matic D Genuine Nissan ATF or equivalent',
                                                            blank=True, null=True)
    power_steering_fluid_recommendation = models.CharField(max_length=100,
                                                           default='type dexron IIE, dexron III or equivalent',
                                                           blank=True, null=True)
    differential_gear_oil_recommendation = models.CharField(max_length=100,
                                                            default='LSD gear oil API gl-5 and SAE 80W-90',
                                                            blank=True, null=True)
    awd_mode_fluid_recommendation = models.CharField(max_length=100,
                                                     default='Nissan Matic D Genuine Nissan ATF or equivalent',
                                                     null=True, blank=True)
    tire_size = models.CharField(max_length=11, default='P245/70R16', blank=True, null=True)
    tire_pressure_front = models.IntegerField(default=29, blank=True, null=True)
    tire_pressure_rear = models.IntegerField(default=29, blank=True, null=True)

    def __str__(self):
        return str(self.title) + ', ' + str(self.serial_number)


class CenterEngine(models.Model):
    # Marine Engine
    serial_number = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True)
    in_hours = models.BooleanField(default=True)
    engine_model = models.CharField(max_length=122, null=True, blank=True)
    original = models.BooleanField(default=True)
    year = models.CharField(max_length=4, choices=YEAR_CHOICES, default='1999')
    horsepower = models.PositiveIntegerField(default=0)
    outboard = models.BooleanField(default=False)
    inboard = models.BooleanField(default=False)
    number_of_cylinders = models.IntegerField(default=4)
    fuel_type = models.CharField(max_length=1, choices=FUEL_CHOICES, default='G')
    fuel_tank_capacity = models.DecimalField(max_digits=6, decimal_places=2, default='21.13')
    engine_oil_mark = models.CharField(max_length=20, default='mark SAE 5W-30')
    engine_oil_capacity = models.DecimalField(decimal_places=2, max_digits=6, default=3.88, help_text='in quarts')

    # visual of engine
    image = models.ImageField(upload_to=upload_center_engine_location, null=True, blank=True, width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField('Description/Conditions/Note', blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.serial_number)


class PortEngine(models.Model):
    # Marine Engine
    serial_number = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True)
    in_hours = models.BooleanField(default=True)
    engine_model = models.CharField(max_length=122, null=True, blank=True)
    original = models.BooleanField(default=True)
    year = models.CharField(max_length=4, choices=YEAR_CHOICES, default='1999')
    horsepower = models.PositiveIntegerField(default=0)
    outboard = models.BooleanField(default=False)
    inboard = models.BooleanField(default=False)
    number_of_cylinders = models.IntegerField(default=4)
    fuel_type = models.CharField(max_length=1, choices=FUEL_CHOICES, default='G')
    fuel_tank_capacity = models.DecimalField(max_digits=6, decimal_places=2, default='21.13')
    engine_oil_mark = models.CharField(max_length=20, default='mark SAE 5W-30')
    engine_oil_capacity = models.DecimalField(decimal_places=2, max_digits=6, default=3.88, help_text='in quarts')

    # visual of engine
    image = models.ImageField(upload_to=upload_port_engine_location, null=True, blank=True, width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField('Description/Conditions/Note', blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.serial_number)


class PortEngine2(models.Model):
    # Marine Engine
    serial_number = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True)
    in_hours = models.BooleanField(default=True)
    engine_model = models.CharField(max_length=122, null=True, blank=True)
    original = models.BooleanField(default=True)
    year = models.CharField(max_length=4, choices=YEAR_CHOICES, default='1999')
    horsepower = models.PositiveIntegerField(default=0)
    outboard = models.BooleanField(default=False)
    inboard = models.BooleanField(default=False)
    number_of_cylinders = models.IntegerField(default=4)
    fuel_type = models.CharField(max_length=1, choices=FUEL_CHOICES, default='G')
    fuel_tank_capacity = models.DecimalField(max_digits=6, decimal_places=2, default='21.13')
    engine_oil_mark = models.CharField(max_length=20, default='mark SAE 5W-30')
    engine_oil_capacity = models.DecimalField(decimal_places=2, max_digits=6, default=3.88, help_text='in quarts')

    # visual of engine
    image = models.ImageField(upload_to=upload_port_engine2_location, null=True, blank=True, width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField('Description/Conditions/Note', blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.serial_number)


class PortEngine3(models.Model):
    # Marine Engine
    serial_number = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True)
    in_hours = models.BooleanField(default=True)
    engine_model = models.CharField(max_length=122, null=True, blank=True)
    original = models.BooleanField(default=True)
    year = models.CharField(max_length=4, choices=YEAR_CHOICES, default='1999')
    horsepower = models.PositiveIntegerField(default=0)
    outboard = models.BooleanField(default=False)
    inboard = models.BooleanField(default=False)
    number_of_cylinders = models.IntegerField(default=4)
    fuel_type = models.CharField(max_length=1, choices=FUEL_CHOICES, default='G')
    fuel_tank_capacity = models.DecimalField(max_digits=6, decimal_places=2, default='21.13')
    engine_oil_mark = models.CharField(max_length=20, default='mark SAE 5W-30')
    engine_oil_capacity = models.DecimalField(decimal_places=2, max_digits=6, default=3.88, help_text='in quarts')

    # visual of engine
    image = models.ImageField(upload_to=upload_port_engine3_location, null=True, blank=True, width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField('Description/Conditions/Note', blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.serial_number)


class StarboardEngine(models.Model):
    # Marine Engine
    serial_number = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True)
    in_hours = models.BooleanField(default=True)
    engine_model = models.CharField(max_length=122, null=True, blank=True)
    original = models.BooleanField(default=True)
    year = models.CharField(max_length=4, choices=YEAR_CHOICES, default='1999')
    horsepower = models.PositiveIntegerField(default=0)
    outboard = models.BooleanField(default=False)
    inboard = models.BooleanField(default=False)
    number_of_cylinders = models.IntegerField(default=4)
    fuel_type = models.CharField(max_length=1, choices=FUEL_CHOICES, default='G')
    fuel_tank_capacity = models.DecimalField(max_digits=6, decimal_places=2, default='21.13')
    engine_oil_mark = models.CharField(max_length=20, default='mark SAE 5W-30')
    engine_oil_capacity = models.DecimalField(decimal_places=2, max_digits=6, default=3.88, help_text='in quarts')

    # visual of engine
    image = models.ImageField(upload_to=upload_starboard_engine_location,
                              null=True, blank=True, width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField('Description/Conditions/Note', blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.serial_number)


class StarboardEngine2(models.Model):
    # Marine Engine
    serial_number = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True)
    in_hours = models.BooleanField(default=True)
    engine_model = models.CharField(max_length=122, null=True, blank=True)
    original = models.BooleanField(default=True)
    year = models.CharField(max_length=4, choices=YEAR_CHOICES, default='1999')
    horsepower = models.PositiveIntegerField(default=0)
    outboard = models.BooleanField(default=False)
    inboard = models.BooleanField(default=False)
    number_of_cylinders = models.IntegerField(default=4)
    fuel_type = models.CharField(max_length=1, choices=FUEL_CHOICES, default='G')
    fuel_tank_capacity = models.DecimalField(max_digits=6, decimal_places=2, default='21.13')
    engine_oil_mark = models.CharField(max_length=20, default='mark SAE 5W-30')
    engine_oil_capacity = models.DecimalField(decimal_places=2, max_digits=6, default=3.88, help_text='in quarts')

    # visual of engine
    image = models.ImageField(upload_to=upload_starboard_engine2_location, null=True,
                              blank=True, width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField('Description/Conditions/Note', blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.serial_number)


class StarboardEngine3(models.Model):
    # Marine Engine
    serial_number = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True)
    in_hours = models.BooleanField(default=True)
    engine_model = models.CharField(max_length=122, null=True, blank=True)
    original = models.BooleanField(default=True)
    year = models.CharField(max_length=4, choices=YEAR_CHOICES, default='1999')
    horsepower = models.PositiveIntegerField(default=0)
    outboard = models.BooleanField(default=False)
    inboard = models.BooleanField(default=False)
    number_of_cylinders = models.IntegerField(default=4)
    fuel_type = models.CharField(max_length=1, choices=FUEL_CHOICES, default='G')
    fuel_tank_capacity = models.DecimalField(max_digits=6, decimal_places=2, default='21.13')
    engine_oil_mark = models.CharField(max_length=20, default='mark SAE 5W-30')
    engine_oil_capacity = models.DecimalField(decimal_places=2, max_digits=6, default=3.88, help_text='in quarts')

    # visual of engine
    image = models.ImageField(upload_to=upload_starboard_engine3_location, null=True,
                              blank=True, width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField('Description/Conditions/Note', blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.serial_number)


class Auxiliary(models.Model):
    # Marine Engine
    serial_number = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True)
    in_hours = models.BooleanField(default=True)
    engine_model = models.CharField(max_length=122, null=True, blank=True)
    original = models.BooleanField(default=True)
    year = models.CharField(max_length=4, choices=YEAR_CHOICES, default='1999')
    horsepower = models.PositiveIntegerField(default=0)
    outboard = models.BooleanField(default=False)
    inboard = models.BooleanField(default=False)
    number_of_cylinders = models.IntegerField(default=4)
    fuel_type = models.CharField(max_length=1, choices=FUEL_CHOICES, default='G')
    fuel_tank_capacity = models.DecimalField(max_digits=6, decimal_places=2, default='21.13')
    engine_oil_mark = models.CharField(max_length=20, default='mark SAE 5W-30')
    engine_oil_capacity = models.DecimalField(decimal_places=2, max_digits=6, default=3.88, help_text='in quarts')

    # visual of engine
    image = models.ImageField(upload_to=upload_auxiliary_location, null=True, blank=True, width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField('Description/Conditions/Note', blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.serial_number)


class GenSet(models.Model):
    # Marine Engine
    serial_number = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True)
    in_hours = models.BooleanField(default=True)
    engine_model = models.CharField(max_length=122, null=True, blank=True)
    original = models.BooleanField(default=True)
    year = models.CharField(max_length=4, choices=YEAR_CHOICES, default='1999')
    horsepower = models.PositiveIntegerField(default=0)
    portable = models.BooleanField(default=False)
    number_of_cylinders = models.IntegerField(default=4)
    fuel_type = models.CharField(max_length=1, choices=FUEL_CHOICES, default='G')
    fuel_tank_capacity = models.DecimalField(max_digits=6, decimal_places=2, default='21.13')
    engine_oil_mark = models.CharField(max_length=20, default='mark SAE 5W-30')
    engine_oil_capacity = models.DecimalField(decimal_places=2, max_digits=6, default=3.88, help_text='in quarts')
    kwatts = models.PositiveIntegerField(default=0)

    # visual of engine
    image = models.ImageField(upload_to=upload_genset_location, null=True, blank=True, width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField('Description/Conditions/Note', blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.serial_number)


class GenSet2(models.Model):
    # Marine Engine
    serial_number = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True)
    in_hours = models.BooleanField(default=True)
    engine_model = models.CharField(max_length=122, null=True, blank=True)
    original = models.BooleanField(default=True)
    year = models.CharField(max_length=4, choices=YEAR_CHOICES, default='1999')
    horsepower = models.PositiveIntegerField(default=0)
    portable = models.BooleanField(default=False)
    number_of_cylinders = models.IntegerField(default=4)
    fuel_type = models.CharField(max_length=1, choices=FUEL_CHOICES, default='G')
    fuel_tank_capacity = models.DecimalField(max_digits=6, decimal_places=2, default='21.13')
    engine_oil_mark = models.CharField(max_length=20, default='mark SAE 5W-30')
    engine_oil_capacity = models.DecimalField(decimal_places=2, max_digits=6, default=3.88, help_text='in quarts')
    kwatts = models.PositiveIntegerField(default=0)

    # visual of engine
    image = models.ImageField(upload_to=upload_genset2_location, null=True, blank=True, width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField('Description/Conditions/Note', blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.serial_number)


class Tools(models.Model):
    # Tools
    title = models.CharField(max_length=35, default='tool name')
    serial_number = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True)
    in_hours = models.BooleanField(default=True)
    engine_model = models.CharField(max_length=122, null=True, blank=True)
    original = models.BooleanField(default=True)
    year = models.CharField(max_length=4, choices=YEAR_CHOICES, default='1999')
    horsepower = models.PositiveIntegerField(default=0)
    number_of_cylinders = models.IntegerField(default=4)
    fuel_type = models.CharField(max_length=1, choices=FUEL_CHOICES, default='G')
    fuel_tank_capacity = models.DecimalField(max_digits=6, decimal_places=2, default='21.13')
    engine_oil_mark = models.CharField(max_length=20, default='mark SAE 5W-30')
    engine_oil_capacity = models.DecimalField(decimal_places=2, max_digits=6, default=3.88, help_text='in quarts')
    kwatts = models.PositiveIntegerField(default=0, blank=True, null=True)

    # visual of tool
    image = models.ImageField(upload_to=upload_tool_location, null=True, blank=True, width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField('Description/Conditions/Note', blank=True)
    publish = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name_plural = 'tools'



# Engine Room inventory
class EngineQuerySet(models.QuerySet):
    def not_draft(self):
        return self.filter(draft=False)

    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                    Q(slug__icontains=query) |
                    Q(content__icontains=query) |
                    Q(asset__icontains=query) |
                    Q(engine_year__icontains=query) |
                    Q(content__icontains=query) |
                    Q(engine_model__icontains=query) |
                    Q(mileage__icontains=query) |
                    Q(amount_of_oil_needed__iexact=query) |
                    Q(number_of_cylinders__icontains=query) |
                    Q(fuel_type__iexact=query) |
                    Q(need_repairs__icontains=query) |
                    Q(user__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs


class EngineManager(models.Manager):
    def get_queryset(self):
        return EngineQuerySet(self.model, using=self._db)

    def active(self, *args, **kwargs):
        # TypeOfAsset.objects.all() = super(PostManager, self).all()
        return self.get_queryset().all()

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class Engines(models.Model):
    # Engine on an engine Room and equipment Specifics on each engine room
    title = models.CharField(max_length=35, default='3.3L 6cyl', blank=True, help_text='name of the room')
    slug = models.SlugField(null=True, blank=True, unique=True, help_text='leave blank, or unique name')
    main = models.ForeignKey(MainEngine, on_delete=models.SET_NULL, null=True, blank=True)
    center = models.ForeignKey(CenterEngine, on_delete=models.SET_NULL, null=True, blank=True)
    port = models.ForeignKey(PortEngine, on_delete=models.SET_NULL, null=True, blank=True)
    port2 = models.ForeignKey(PortEngine2, on_delete=models.SET_NULL, null=True, blank=True)
    port3 = models.ForeignKey(PortEngine3, on_delete=models.SET_NULL, null=True, blank=True)
    starboard = models.ForeignKey(StarboardEngine, on_delete=models.SET_NULL, null=True, blank=True)
    starboard2 = models.ForeignKey(StarboardEngine2, on_delete=models.SET_NULL, null=True, blank=True)
    starboard3 = models.ForeignKey(StarboardEngine3, on_delete=models.SET_NULL, null=True, blank=True)
    auxiliary = models.ForeignKey(Auxiliary, on_delete=models.SET_NULL, null=True, blank=True)
    genset = models.ForeignKey(GenSet, on_delete=models.SET_NULL, null=True, blank=True)
    genset2 = models.ForeignKey(GenSet2, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, null=True, on_delete=models.SET_NULL)
    engineer = models.ManyToManyField(Engineer, blank=True)
    tool_and_equipment = models.ManyToManyField(Tools, blank=True)

    # Engine Location
    engine_on = models.ForeignKey(TypeOfAsset, on_delete=models.SET_NULL, null=True)

    # visual of Asset
    image = models.ImageField(upload_to=upload_engine_room_location, null=True, blank=True, width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField('Description/Conditions/Note', blank=True)

    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    publish = models.DateTimeField(auto_now=True, auto_now_add=False)

    objects = EngineManager()

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = 'engine of'
        verbose_name_plural = 'engine specs'

    def __str__(self):
        return str(self.title)

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    def get_absolute_url(self):
        return reverse("engine_room:detail", kwargs={"slug": self.slug})

    def get_api_url(self, request=None):
        return api_reverse("api-engine_room:engine-rud",  kwargs={'slug': self.slug}, request=request)

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    @property
    def owner(self):
        return self.user


def create_slug_engine(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Engines.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug_engine(instance, new_slug=new_slug)
    return slug


def pre_save_engine_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug_engine(instance)

    if instance.content:
        html_string = instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var


pre_save.connect(pre_save_engine_receiver, sender=Engines)
