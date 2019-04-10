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
from shops.models import Shop

User = settings.AUTH_USER_MODEL
# Create your models here.


def upload_property_location(instance, filename):
    property_asset_model = instance.__class__
    new_id = property_asset_model.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


def upload_building_location(instance, filename):
    building_model = instance.__class__
    new_id = building_model.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


class BuildingLocationQuerySet(models.QuerySet):
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


class LocationManager(models.Manager):
    def get_queryset(self):
        return BuildingLocationQuerySet(self.model, using=self._db)

    def published(self):
        return self.filter(publish__lte=timezone.now().not_draft())

    def active(self):
        # TypeOfAsset.objects.all() = super(PostManager, self).all()
        return self.get_queryset().published()

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class Property(models.Model):
    title = models.CharField(max_length=100, help_text="name of property", default='ranch name')

    # gps location
    location = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)

    # visual of Asset
    image = models.ImageField(upload_to=upload_property_location, null=True, blank=True, width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField('description and condition')

    # Time Stamp
    publish = models.DateField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    # if Draft = not finished do not publish
    draft = models.BooleanField(default=False)

    # description of Building
    acre = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text='size of property')

    def __str__(self):
        return str(self.title)


class BuildingLocation(models.Model):
    title = models.CharField(max_length=30, blank=True, null=True, help_text='name of the building')
    slug = models.SlugField(null=True, blank=True, unique=True, help_text='leave blank, or unique name')
    on_location = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True)

    # Owner of Asset
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, help_text='person responsible for')

    # visual of Asset
    image = models.ImageField(upload_to=upload_building_location, null=True, blank=True, width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField('description and condition')

    # Time Stamp
    publish = models.DateField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    # if Draft = not finished do not publish
    draft = models.BooleanField(default=False)

    # description of Building
    square_feet = models.IntegerField(help_text='building area')

    objects = LocationManager()

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("property:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["user", "-publish"]

    def get_api_url(self, request=None):
        return api_reverse("api-property:asset-rud", kwargs={'slug': self.slug}, request=request)

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
    qs = BuildingLocation.objects.filter(slug=slug).order_by("-id")
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


pre_save.connect(pre_save_asset_receiver, sender=BuildingLocation)


def rl_post_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        instance.save()


post_save.connect(rl_post_save_receiver, sender=BuildingLocation)
