from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from rest_framework.reverse import reverse as api_reverse

from comments.models import Comment
from markdown_deux import markdown

from assets.models import TypeOfAsset
from .utils import get_read_time, unique_slug_generator

# Create your models here.


User = settings.AUTH_USER_MODEL


def upload_location(instance, filename):
    fuel_station_model = instance.__class__
    new_id = fuel_station_model.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


class FuelStationQuerySet(models.QuerySet):
    def not_draft(self):
        return self.filter(draft=False)

    def published(self):
        return self.filter(publish__lte=timezone.now().not_draft())

    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                    Q(title__icontains=query) |
                    Q(slug__icontains=query) |
                    Q(invoice_number__iexact=query) |
                    Q(content__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs


class FuelStationManager(models.Manager):
    def get_queryset(self):
        return FuelStationQuerySet(self.model, using=self._db)

    def active(self, *args, **kwargs):
        # Post.objects.all() = super(PostManager, self).all()
        return self.get_queryset().published()

    def search(self, query=None):
        return self.get_queryset().search(query=query)


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


class FuelStation(models.Model):
    # defines fuel consumption of each vehicle
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    title = models.CharField('fuel station name', max_length=120)
    slug = models.SlugField(null=True, blank=True, unique=True, help_text='leave blank or your-brand-name')

    # Relate invoice and vehicle
    vehicle = models.ForeignKey(TypeOfAsset, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=255)
    date = models.DateTimeField()

    # consumable
    fuel_type_pumped = models.CharField(max_length=2, choices=FUEL_TYPE_CHOICES, default='gasoline-86')
    price_per_gal = models.DecimalField(max_digits=4, decimal_places=3)
    amount_of_fuel = models.DecimalField(max_digits=8, decimal_places=3)
    fuel_total = models.DecimalField(max_digits=6, decimal_places=2)

    current_miles = models.DecimalField('miles ran', max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now=True)

    fueled_by = models.CharField(max_length=120, null=True, blank=True)
    draft = models.BooleanField(default=False)
    publish = models.DateTimeField(auto_now=True, auto_now_add=False)

    # image
    image = models.ImageField(upload_to=upload_location, null=True, blank=True, width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0, null=True)
    width_field = models.IntegerField(default=0, null=True)
    content = models.TextField('Special Remark')

    object = FuelStationManager

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("fuel_station:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-timestamp", "-publish"]

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    def get_api_url(self, request=None):
        return api_reverse("api-fuel_station:fuel-rud",  kwargs={'slug': self.slug}, request=request)

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
    qs = FuelStation.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.content:
        html_string = instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var


pre_save.connect(pre_save_post_receiver, sender=FuelStation)


def rl_post_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        instance.save()


post_save.connect(rl_post_save_receiver, sender=FuelStation)