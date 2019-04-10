from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from rest_framework.reverse import reverse as api_reverse
from django.db.models import Q

from markdown_deux import markdown
from comments.models import Comment

from .utils import get_read_time, unique_slug_generator

from providers.models import Supplier

from property.models import BuildingLocation

User = settings.AUTH_USER_MODEL
# Create your models here.


def upload_location(instance, filename):
    asset_model = instance.__class__
    new_id = asset_model.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


def parts_upload(instance, filename):
    asset_model = instance.__class__
    new_id = asset_model.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


def marine_vessel(instance, filename):
    marine_model = instance.__class__
    new_id = marine_model.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


class AssetQuerySet(models.QuerySet):
    def not_draft(self):
        return self.filter(draft=False)

    def published(self):
        return self.filter(publish__lte=timezone.now().not_draft())

    def marine_vessel(self):
        return self.filter(marine_vessel=True)

    def aircraft(self):
        return self.filter(air_craft=True)

    def land_vessel(self):
        return self.filter(land_vessel=True)

    def tool(self):
        return self.filter(tool=True)

    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                    Q(title__icontains=query) |
                    Q(slug__icontains=query) |
                    Q(content__icontains=query) |
                    Q(user__iexact=query) |
                    Q(brand__icontains=query) |
                    Q(model__icontains=query) |
                    Q(year__iexact=query) |
                    Q(color__icontains=query) |
                    Q(vin__iexact=query) |
                    Q(vin__icontains=query) |
                    Q(registration__iexact=query) |
                    Q(registration__icontains=query) |
                    Q(license_plate__iexact=query) |
                    Q(license_plate__icontains=query) |
                    Q(used_for__icontains=query) |
                    Q(content__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs


class AssetManager(models.Manager):
    def get_queryset(self):
        return AssetQuerySet(self.model, using=self._db)

    def published(self):
        return self.filter(publish__lte=timezone.now().not_draft())

    def active(self):
        # TypeOfAsset.objects.all() = super(PostManager, self).all()
        return self.get_queryset().published()

    def marine(self):
        return self.get_queryset().marine_vessel()

    def search(self, query=None):
        return self.get_queryset().search(query=query)

    def land(self):
        return self.get_queryset().land_vessel()

    def air(self):
        return self.get_queryset().aircraft()


FUEL_CHOICES = (
    ('G', 'gasoline'),
    ('D', 'diesel'),
    ('M', 'mix two cycle'),
    ('E', 'electric'),
    ('H', 'hybrid'),
    ('W', 'wind'),
    ('P', 'human powered'),
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


TYPE_OF_VEHICLE = (
    ('Cr', 'cars'),
    ('T', 'trucks'),
    ('Bu', 'buses'),
    ('At', "off road ATV's"),
    ('Mc', 'motorcycles'),
    ('Sn', 'snowmobiles'),
    ('Tc', 'tractors'),
    ('Bu', 'bulldozers'),
    ('Se', 'seed drills'),
    ('BL', 'backhoe loaders'),
    ('Co', 'continuous tracks'),
    ('HE', 'hydraulic excavators'),
    ('DT', 'dump trucks'),
    ('WD', 'wheel dozers'),
    ('DL', 'drag liners'),
    ('SK', 'skid-steer loaders'),
    ('MG', 'motor graders'),
    ('CL', 'crawler loaders'),
    ('Tr', 'Trenchers'),
    ('AT', 'articulated trucks'),
    ('AP', 'asphalt pavers'),
    ('CP', 'cold planers'),
    ('CT', 'compact tracks'),
    ('MT', 'multi-terrain loaders'),
    ('Co', 'compactors'),
    ('Ex', 'excavetors'),
    ('FB', 'feller bunchers'),
    ('F', 'forwarders'),
    ('H', 'harvesters'),
    ('KL', 'knuckleboom loaders'),
    ('Lo', 'loaders'),
    ('OT', 'off-highway trucks'),
    ('Sk', 'skidders'),
    ('Te', 'telehandlers'),
    ('WT', 'wheel tracktor-scrapers'),
    ('PW', 'power plants'),
)


MARINE_CLASSIFICATION_CHOICE = (
    ('UPV', 'uninspected passenger vessels'),
    ('IPV', 'inspected passenger vessels'),
    ('PWC', 'personal water craft'),
)


HULL_TYPE = (
    ('MV', 'mono hull deep V'),
    ('MF', 'mono hull flat bottom'),
    ('CD', 'catamaran double hull'),
    ('CT', 'catamaran triple hull'),
)


HULL_MATERIAL = (
    ('F', 'fiberglass'),
    ('W', 'wood'),
    ('A', 'aluminum'),
    ('S', 'steel'),
    ('C', 'cement'),
    ('K', 'kevlar'),
)


BODY_TYPE_CHOICES = (
    ('UT', 'utility'),
    ('SP', 'sport'),
    ('4D', 'four door'),
    ('VY', 'v drive motor Yacht'),
    ('WA', 'walk around'),
    ('BR', 'bow rider'),
    ('FB', 'flat bottom'),
    ('CT', 'catamaran')
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
    ('1982', '1982'),
    ('1981', '1981'),
    ('1980', '1980'),
    ('1979', '1979'),
    ('1978', '1978'),
    ('1977', '1977'),
    ('1976', '1976'),
    ('1975', '1975'),
    ('1974', '1974'),
    ('1973', '1973'),
    ('1972', '1972'),
    ('1971', '1971'),
    ('1970', '1970'),
    ('1969', '1969'),
    ('1968', '1968'),
    ('1967', '1967'),
    ('1966', '1966'),
    ('1965', '1965'),
    ('1964', '1964'),
    ('1963', '1963'),
    ('1962', '1962'),
    ('1961', '1961'),
    ('1960', '1960'),
    ('1959', '1959'),
    ('1958', '1958'),
    ('1957', '1957'),
    ('1956', '1956'),
    ('1955', '1955'),
    ('1954', '1954'),
    ('1953', '1953'),
    ('1952', '1952'),
    ('1951', '1951'),
    ('1950', '1950'),
    ('1949', '1949'),
    ('1948', '1948'),
    ('1947', '1947'),
    ('1946', '1946'),
    ('1946', '1945'),
    ('1944', '1944'),
    ('1943', '1943'),
    ('1942', '1942'),
    ('1941', '1941'),
    ('1940', '1940'),
    ('1939', '1939'),
    ('1938', '1938'),
    ('1937', '1937'),
    ('1936', '1936'),
    ('1935', '1935'),
    ('1934', '1934'),
    ('1933', '1933'),
    ('1932', '1932'),
    ('1931', '1931'),
    ('1930', '1930'),
    ('1929', '1929'),
    ('1928', '1928'),
    ('1927', '1927'),
    ('1926', '1926'),
    ('1925', '1925'),
    ('1924', '1924'),
    ('1923', '1923'),
    ('1922', '1922'),
    ('1921', '1921'),
    ('1920', '1920'),
    ('1919', '1919'),
    ('1918', '1918'),
    ('1917', '1917'),
    ('1916', '1916'),
    ('1915', '1915'),
    ('1914', '1914'),
    ('1913', '1913'),
    ('1912', '1912'),
    ('1911', '1911'),
    ('1910', '1910'),
    ('1909', '1909'),
    ('1908', '1908'),
    ('1907', '1907'),
    ('1906', '1906'),
    ('1905', '1905'),
    ('1904', '1904'),
    ('1903', '1903'),
    ('1902', '1902'),
    ('1901', '1901')
)


CAR_MAKE_CHOICES = (
    ('se', 'select make'),
    ('ac', 'acura'),
    ('am', 'am general'),
    ('au', 'audi'),
    ('be', 'bentley'),
    ('bm', 'bmw'),
    ('bu', 'buick'),
    ('ca', 'cadillac'),
    ('ch', 'chevrolet'),
    ('cr', 'chrysler'),
    ('da', 'daewoo'),
    ('do', 'dodge'),
    ('fe', 'ferrari'),
    ('fo', 'ford'),
    ('fr', 'freightliner'),
    ('gm', 'gmc'),
    ('ho', 'honda'),
    ('hy', 'hyundai'),
    ('in', 'infiniti'),
    ('it', 'international'),
    ('is', 'isuzu'),
    ('ja', 'jaguar'),
    ('je', 'jeep'),
    ('ki', 'kia'),
    ('la', 'lamborghini'),
    ('lr', 'land rover'),
    ('le', 'lexus'),
    ('li', 'lincoln'),
    ('lo', 'lotus'),
    ('ma', 'mazda'),
    ('me', 'mercedes benz'),
    ('mr', 'mercury'),
    ('mi', 'mitsubishi'),
    ('ni', 'nissan'),
    ('ol', 'oldsmobile'),
    ('pl', 'plymouth'),
    ('po', 'pontiac'),
    ('pr', 'porsche'),
    ('ro', 'rolls royce'),
    ('sa', 'saab'),
    ('st', 'saturn'),
    ('st', 'sterling'),
    ('su', 'subaru'),
    ('sz', 'suzuki'),
    ('to', 'toyota'),
    ('vw', 'volkswagen'),
    ('vo', 'volvo')
)


WHEELS = (
    ('A', 'alloy'),
    ('C', 'cast iron')
)


class Parts(models.Model):
    title = models.CharField('part name', max_length=35)
    part_number = models.CharField(max_length=17, unique=True)

    # Part Image
    image = models.ImageField(upload_to=parts_upload, null=True, blank=True, width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField('Part description')
    used_for = models.CharField(max_length=200)

    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    publish = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title) + (str(self.part_number))

    def get_absolute_url(self):
        return reverse("assets:part_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["title", 'part_number']

    def get_api_url(self, request=None):
        return api_reverse("api-assets:asset-marine-parts-rud", kwargs={'pk': self.pk}, request=request)


class Asset(models.Model):
    serial_number = models.CharField('engine serial number', max_length=17, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                             help_text='person responsible for')
    odometer = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    in_miles = models.BooleanField(default=False)
    in_kilometers = models.BooleanField(default=False)
    in_hours = models.BooleanField(default=False)

    def __str__(self):
        return str(self.serial_number + ', ' + str(self.odometer))

    def get_absolute_url(self):
        return reverse("assets:asset_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ['user']

    def get_api_url(self, request=None):
        return api_reverse("api-assets:asset-rud", kwargs={'pk': self.pk}, request=request)

    @property
    def owner(self):
        return self.user


class CarManufacturer(models.Model):
    title = models.CharField('make', choices=CAR_MAKE_CHOICES, max_length=2, default="se")

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("assets:car-manufacturer_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["title"]

    def get_api_url(self, request=None):
        return api_reverse("api-assets:asset-car-manufacturer-rud", kwargs={'pk': self.pk}, request=request)


class HeavyEquipmentManufacturer(models.Model):
    title = models.CharField('make', max_length=60, unique=True)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("assets:heavy-manufacturer_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["title"]

    def get_api_url(self, request=None):
        return api_reverse("api-assets:asset-heavy-manufacturer-rud", kwargs={'pk': self.pk}, request=request)


class HeavyEquipmentModelType(models.Model):
    title = models.CharField('model', max_length=60)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("assets:heavy-model_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["title"]

    def get_api_url(self, request=None):
        return api_reverse("api-assets:asset-heavy-model-rud", kwargs={'pk': self.pk}, request=request)


class MarineVesselManufacturer(models.Model):
    title = models.CharField('brand', max_length=60, unique=True)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("assets:marine-manufacturer_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["title"]

    def get_api_url(self, request=None):
        return api_reverse("api-assets:asset-marine-manufacturer-rud", kwargs={'pk': self.pk}, request=request)


class EquipmentManufacturer(models.Model):
    title = models.CharField('brand', max_length=60, unique=True)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("assets:equipment-manufacturer_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["title"]

    def get_api_url(self, request=None):
        return api_reverse("api-assets:asset-equipment-manufacturer-rud", kwargs={'pk': self.pk}, request=request)


class CarModelType(models.Model):
    title = models.CharField('model', max_length=60)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("assets:car-model_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["title"]

    def get_api_url(self, request=None):
        return api_reverse("api-assets:asset-car-model-rud", kwargs={'pk': self.pk}, request=request)


class MarineModelType(models.Model):
    title = models.CharField('model', max_length=60)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("assets:marine-model_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["title"]

    def get_api_url(self, request=None):
        return api_reverse("api-assets:asset-marine-model-rud", kwargs={'pk': self.pk}, request=request)


class EquipmentModelType(models.Model):
    title = models.CharField('model', max_length=60)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("assets:equipment-model_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["title"]

    def get_api_url(self, request=None):
        return api_reverse("api-assets:asset-equipment-model-rud", kwargs={'pk': self.pk}, request=request)


class ThroughHull(models.Model):
    title = models.CharField('through hole purpose', max_length=100, help_text='center engine strainer')
    part = models.ForeignKey(Parts, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.title) + str(self.part)

    def get_absolute_url(self):
        return reverse("assets:through-hull_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["title", 'part']

    def get_api_url(self, request=None):
        return api_reverse("api-assets:asset-marine-through-hull-rud", kwargs={'pk': self.pk}, request=request)


class MarineVessel(models.Model):
    title = models.CharField(max_length=30, blank=True, null=True, help_text='name of the vessel')
    slug = models.SlugField(null=True, blank=True, unique=True, help_text='leave blank, or unique name')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                             help_text='person responsible for')
    asset = models.ManyToManyField(Asset)

    # Certificate of Vehicle Registration
    port_of_registry = models.CharField(max_length=100, blank=True, null=True)
    reg_exp_date = models.DateField(blank=True, null=True)
    vehicle_classification = models.CharField(choices=MARINE_CLASSIFICATION_CHOICE, max_length=3, default='PV')

    # maker
    brand = models.ForeignKey(MarineVesselManufacturer, on_delete=models.SET_NULL, null=True)
    model = models.ForeignKey(MarineModelType, on_delete=models.SET_NULL, null=True)
    year = models.CharField('year built', max_length=4, choices=YEAR_CHOICES, default='2019')
    gross_weight = models.PositiveIntegerField(blank=True, null=True)
    hull_number = models.CharField(max_length=17)
    hull_type = models.CharField(choices=HULL_TYPE, default='MV', max_length=2)
    hull_material = models.CharField(choices=HULL_MATERIAL, max_length=1, default='F')

    # through holes and propulsion
    number_of_through_holes = models.ManyToManyField(ThroughHull, blank=True)

    # Marine Vessel Image
    image = models.ImageField(upload_to=marine_vessel, null=True, blank=True, width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField('description and condition')
    used_for = models.CharField(max_length=100)

    # Registered to
    registered_owner = models.CharField(max_length=25, default='Owner')
    owners_address = models.CharField(max_length=120, default='address')

    # Insurance Policy
    is_it_insured = models.BooleanField(default=False)
    insurance_provider = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    # insurance_provider = models.CharField(max_length=100, default='GEICO')

    insurance_type = models.CharField(max_length=100, default='marine')
    insurance_cost = models.DecimalField(max_digits=5, decimal_places=2, default=159.26, blank=True)
    insurance_policy_number = models.CharField(max_length=6, blank=True)

    # assistance tow
    seatow = models.BooleanField(default=False)
    assistance_miles = models.IntegerField(default=20, blank=True, null=True)

    # Original MSRP
    original_msrp = models.IntegerField(default=36075, blank=True, null=True)
    price_paid = models.IntegerField(default=400, help_text='in dollars', blank=True, null=True)

    # Vessel dimensions
    reported_loa = models.PositiveIntegerField(blank=True, null=True)
    reported_lwl = models.PositiveIntegerField(blank=True, null=True)
    reported_beam = models.PositiveIntegerField(blank=True, null=True)
    reported_draft = models.PositiveIntegerField(blank=True, null=True)
    max_height = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("assets:marine_detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["user", "brand", "model", "year"]

    def get_api_url(self, request=None):
        return api_reverse("api-assets:asset-marine-rud", kwargs={'slug': self.slug}, request=request)

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

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    @property
    def owner(self):
        return self.user


def pre_save_marine_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.content:
        html_string = instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var


pre_save.connect(pre_save_marine_receiver, sender=MarineVessel)


def rl_post_save_auto_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        instance.save()


post_save.connect(rl_post_save_auto_receiver, sender=MarineVessel)


class Automobile(models.Model):
    title = models.CharField('name of asset', max_length=100)
    slug = models.SlugField(null=True, blank=True, unique=True, help_text='leave blank, or unique name')
    asset = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True)
    engineering_equipment = models.CharField(choices=TYPE_OF_VEHICLE, max_length=2, default='Cr')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                             help_text='person responsible for')

    brand = models.ForeignKey(CarManufacturer, on_delete=models.SET_NULL, null=True)
    model = models.ForeignKey(CarModelType, on_delete=models.SET_NULL, null=True)
    year = models.CharField('year built', max_length=4, choices=YEAR_CHOICES, default='2019')
    gross_weight = models.PositiveIntegerField(blank=True, null=True)
    # odometer = models.ForeignKey(MainEngine, on_delete=models.SET_NULL, null=True)

    # visual of Asset
    image = models.ImageField(upload_to=upload_location, null=True, blank=True, width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField('description and condition')

    # description of Asset
    used_for = models.CharField(max_length=120)
    color = models.CharField(max_length=120, null=True, blank=True)

    fuel = models.CharField('type of fuel', choices=FUEL_CHOICES, max_length=1)

    license_plate = models.CharField('tag/licence plate', max_length=17, null=True, blank=True, unique=True)
    # audit_number = models.IntegerField(blank=True, null=True)
    # d_g_v_w = models.IntegerField(default=0)
    vin = models.CharField('vin or hull id', max_length=17, unique=True, default='JNRAR05YX049150')
    fees_paid = models.DecimalField(max_digits=6, decimal_places=2, default=51.00)
    wt_wheels = models.IntegerField(default=4141)
    body_type = models.CharField(choices=BODY_TYPE_CHOICES, max_length=4, default='UT')
    cylinders = models.IntegerField(default=6)

    # Registered to
    registered_owner = models.CharField(max_length=25, default='Owner')
    owners_address = models.CharField(max_length=120, default='address')

    # Insurance Policy
    is_it_insured = models.BooleanField(default=False)
    insurance_provider = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    # insurance_provider = models.CharField(max_length=100, default='GEICO')

    insurance_type = models.CharField(max_length=100, default='auto')
    insurance_cost = models.DecimalField(max_digits=5, decimal_places=2, default=159.26)
    insurance_policy_number = models.CharField(max_length=12)

    emergency_roadside_assistance = models.BooleanField(default=False)
    assistance_miles = models.IntegerField(default=20, blank=True, null=True)

    # vehicle Exterior Dimensions
    wheelbase = models.DecimalField(max_digits=6, decimal_places=2, default=106.3, blank=True, null=True)
    overall_length = models.DecimalField(max_digits=6, decimal_places=2, default=183.9, blank=True, null=True)
    overall_height = models.DecimalField(max_digits=6, decimal_places=2, default=70.7, blank=True, null=True)
    min_ground_clearance = models.DecimalField(max_digits=6, decimal_places=2, default=8.3, blank=True, null=True)
    base_curb_weight = models.DecimalField(max_digits=6, decimal_places=2, default=4352, blank=True, null=True)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("assets:land_detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["user", "brand", "model", "year"]

    def get_api_url(self, request=None):
        return api_reverse("api-assets:asset-land-rud", kwargs={'slug': self.slug}, request=request)

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

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    @property
    def owner(self):
        return self.user


def create_auto_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Automobile.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_auto_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.content:
        html_string = instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var


pre_save.connect(pre_save_auto_receiver, sender=Automobile)


def rl_post_save_auto_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        instance.save()


post_save.connect(rl_post_save_auto_receiver, sender=Automobile)


class Equipment(models.Model):
    title = models.CharField('name of asset', max_length=100)
    slug = models.SlugField(null=True, blank=True, unique=True, help_text='leave blank, or unique name')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                             help_text='person responsible for')
    asset = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True)

    brand = models.ForeignKey(EquipmentManufacturer, on_delete=models.SET_NULL, null=True)
    model = models.ForeignKey(EquipmentModelType, on_delete=models.SET_NULL, null=True)
    year = models.CharField('year built', max_length=4, choices=YEAR_CHOICES, default='2019')
    gross_weight = models.PositiveIntegerField(blank=True, null=True)

    # visual of Asset
    image = models.ImageField(upload_to=upload_location, null=True, blank=True, width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField('description and condition')

    # description of Asset
    used_for = models.CharField(max_length=120)
    color = models.CharField(max_length=120, null=True, blank=True)

    fuel = models.CharField('type of fuel', choices=FUEL_CHOICES, max_length=1)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("assets:equipment_detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["user", "brand", "model", "year"]

    def get_api_url(self, request=None):
        return api_reverse("api-assets:asset-equipment-rud", kwargs={'slug': self.slug}, request=request)

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

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    @property
    def owner(self):
        return self.user


def pre_save_equipment_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.content:
        html_string = instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var


pre_save.connect(pre_save_equipment_receiver, sender=Equipment)


def rl_post_save_equipment_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        instance.save()


post_save.connect(rl_post_save_equipment_receiver, sender=Equipment)


class TypeOfAsset(models.Model):
    # In here we define the type of asset
    # Name identification
    title = models.CharField('name of asset', max_length=100)
    slug = models.SlugField(null=True, blank=True, unique=True, help_text='leave blank, or unique name')
    # Owner of Asset
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                             help_text='person responsible for')

    # visual of Asset
    image = models.ImageField(upload_to=upload_location, null=True, blank=True, width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField('description and condition')

    # asset type
    marine_vessel = models.ForeignKey(MarineVessel, on_delete=models.SET_NULL, null=True)
    land_vehicle = models.ForeignKey(Automobile, on_delete=models.SET_NULL, null=True)
    tool = models.ManyToManyField(Equipment, blank=True)

    # Time Stamp
    publish = models.DateField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    # if Draft = not finished do not publish
    draft = models.BooleanField(default=False)
    location_of_asset = models.ForeignKey(BuildingLocation, on_delete=models.SET_NULL, null=True,
                                          blank=True, help_text='where is the asset')

    objects = AssetManager()

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("assets:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["user", "-publish"]

    def get_api_url(self, request=None):
        return api_reverse("api-assets:asset-rud", kwargs={'slug': self.slug}, request=request)

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

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    @property
    def owner(self):
        return self.user


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = TypeOfAsset.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_asset_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.content:
        html_string = instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var


pre_save.connect(pre_save_asset_receiver, sender=TypeOfAsset)


def rl_post_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        instance.save()


post_save.connect(rl_post_save_receiver, sender=TypeOfAsset)
