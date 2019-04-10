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


class PersonnelQuerySet(models.QuerySet):
    def not_draft(self):
        return self.filter(draft=False)

    def published(self):
        return self.filter(publish__lte=timezone.now().not_draft())

    def crew(self):
        return self.filter(is_crew=True)

    def mechanic(self):
        return self.filter(is_mechanic=True)

    def service_provider(self):
        return self.filter(is_service_provider=True)

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


class PersonnelManager(models.Manager):
    def get_queryset(self):
        return PersonnelQuerySet(self.model, using=self._db)

    def published(self):
        return self.filter(publish__lte=timezone.now().not_draft())

    def active(self):
        # TypeOfAsset.objects.all() = super(PostManager, self).all()
        return self.get_queryset().published()

    def is_mechanic(self):
        return self.get_queryset().mechanic()

    def search(self, query=None):
        return self.get_queryset().search(query=query)

    def is_crew(self):
        return self.get_queryset().crew()

    def service_provider(self):
        return self.get_queryset().service_provider()


class Engineer(models.Model):
    first_name = models.CharField(max_length=35, default='first name')
    last_name = models.CharField(max_length=35, default='last name')
    title = models.CharField(max_length=30, blank=True, null=True, help_text='position')
    slug = models.SlugField(null=True, blank=True, unique=True, help_text='leave blank, or unique name')
    license_no = models.CharField('license number', max_length=17, unique=True, default='123456789')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, null=True, on_delete=models.SET_NULL)

    # define status of employment
    is_crew = models.BooleanField(default=False)
    is_service_provider = models.BooleanField(default=False)
    service_provider = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)

    # contact information
    email = models.EmailField(null=True, blank=True)
    phone = models.IntegerField(blank=True, null=True, help_text='include all numbers')

    # specializes on
    is_mechanic = models.BooleanField(default=False)
    content = models.TextField(blank=True, null=True, help_text='specializes on')

    # rate by hour
    rate = models.PositiveIntegerField(default='65', null=True, blank=True)

    objects = PersonnelManager()

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("assets:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["user", "-rate"]

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
    qs = Engineer.objects.filter(slug=slug).order_by("-id")
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


pre_save.connect(pre_save_asset_receiver, sender=Engineer)


def rl_post_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        instance.save()


post_save.connect(rl_post_save_receiver, sender=Engineer)
