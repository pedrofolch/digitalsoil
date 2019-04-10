from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.urls import reverse
from django.utils.safestring import mark_safe
from rest_framework.reverse import reverse as api_reverse
from comments.models import Comment
from markdown_deux import markdown
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from .utils import get_read_time
from django.db.models.signals import pre_save
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.
YEARS = (
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
)


def upload_location(instance, filename):
    sensor_iot_model = instance.__class__
    new_id = sensor_iot_model.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


def upload_sensor_location(instance, filename):
    sensoriot_model = instance.__class__
    new_id = sensoriot_model.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


class SensorIoTQuerySet(models.QuerySet):
    def not_active(self):
        return self.filter(active=False)

    def activated(self):
        return self.filter(publish__lte=timezone.now().not_active())

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
                    Q(brand__icontains=query) |
                    Q(model__icontains=query) |
                    Q(year__iexact=query) |
                    Q(color__icontains=query) |
                    Q(serial_number__iexact=query) |
                    Q(serial_number__icontains=query) |
                    Q(registration__iexact=query) |
                    Q(registration__icontains=query) |
                    Q(used_for__icontains=query) |
                    Q(content__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs


class SensorIoTManager(models.Manager):
    def get_queryset(self):
        return SensorIoTQuerySet(self.model, using=self._db)

    def active(self):
        # SensorIoT.objects.all() = super(SensorIoTManager, self).all()
        return self.get_queryset()

    def marine(self):
        return self.get_queryset().marine_vessel()

    def search(self, query=None):
        return self.get_queryset().search(query=query)

    def land(self):
        return self.get_queryset().land_vessel()

    def air(self):
        return self.get_queryset().aircraft()


class SensorIoT(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                             help_text='person responsible for')
    # Name and url
    title = models.CharField(max_length=65, default='sensoriot')
    slug = models.SlugField(null=True, blank=True, unique=True, help_text='leave blank, or unique name')
    url = models.URLField(blank=True, null=True)
    address = models.GenericIPAddressField(blank=True, null=True, help_text='ip address')

    # visual of Asset
    image = models.ImageField(upload_to=upload_sensor_location, null=True, blank=True, width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField('description and condition')

    # description of sensor
    brand = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    year = models.CharField(max_length=4, choices=YEARS, default='2019')

    serial_number = models.CharField('serial number', max_length=17, null=True, blank=True, unique=True)
    registration = models.CharField('tag', max_length=17, null=True, blank=True, unique=True)
    used_for = models.CharField(max_length=120)
    color = models.CharField(max_length=120, null=True, blank=True)

    # Time Stamp
    publish = models.DateField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = SensorIoTManager()

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("iotsensor:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-publish", "brand", "model", "year", "user"]

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    def get_api_url(self, request=None):
        return api_reverse("api-iotsensor:iot-rud", kwargs={'slug': self.slug}, request=request)

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


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = SensorIoT.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_sensoriot_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.content:
        html_string = instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var


pre_save.connect(pre_save_sensoriot_receiver, sender=SensorIoT)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    last_scrape = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "{}-{}".format(self.user, self.last_scrape)


class Headline(models.Model):
    title = models.CharField(max_length=225)
    image = models.ImageField(null=True, blank=True, upload_to='upload_location')

    url = models.TextField()

    def __str__(self):
        return self.title
