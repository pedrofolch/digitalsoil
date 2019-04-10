from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db import models
from django.contrib.gis.db import models as gps_models

from django.utils import timezone
from django.utils.safestring import mark_safe
from rest_framework.reverse import reverse as api_reverse
from django.db.models import Q
from django.utils.text import slugify
from django.db.models.signals import pre_save

from markdown_deux import markdown
from comments.models import Comment
from .utils import get_read_time

from assets.models import TypeOfAsset
from providers.models import Supplier
from engine_room.models import Engines
from personnel.models import Engineer

User = settings.AUTH_USER_MODEL

# Create your models here.


def upload_location(instance, filename):
    repair_model = instance.__class__
    new_id = repair_model.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


class RepairQuerySet(models.QuerySet):
    def not_draft(self):
        return self.filter(draft=False)

    def published(self):
        return self.filter(publish__lte=timezone.now().not_draft())

    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                    Q(title__icontains=query) |
                    Q(user__icontains=query) |
                    Q(slug__icontains=query) |
                    Q(po_number__icontains=query) |
                    Q(on_asset__icontains=query) |
                    Q(problem_found__icontains=query) |
                    Q(approved_by__icontains=query) |
                    Q(approved_by__icontains=query) |
                    Q(invoice_number__iexact=query) |
                    Q(invoice_number__icontains=query) |
                    Q(engine__iexact=query) |
                    Q(asset__icontains=query) |
                    Q(estimate_number__iexact=query) |
                    Q(work_order__iexact=query) |
                    Q(license_plate__icontains=query) |
                    Q(used_for__icontains=query) |
                    Q(year__iexact=query) |
                    Q(part_no__icontains=query) |
                    Q(content__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs


class RepairManager(models.Manager):
    def get_queryset(self):
        return RepairQuerySet(self.model, using=self._db)

    def active(self, *args, **kwargs):
        # Post.objects.all() = super(PostManager, self).all()
        return self.get_queryset().published()

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class RepairOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, help_text='main problem')
    slug = models.SlugField(null=True, blank=True, unique=True)

    purchase_order = models.BooleanField(default=False)
    estimate = models.BooleanField(default=False)
    po_number = models.CharField(max_length=25, default='0001', unique=True)
    on_asset = models.ForeignKey(TypeOfAsset, on_delete=models.SET_NULL, null=True)
    problem_found = models.TextField()

    publish = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    approved_by = models.CharField(max_length=25, default='myself')

    assigned_to = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    preferred_engineer = models.ForeignKey(Engineer, on_delete=models.SET_NULL, null=True, blank=True)
    # asset_location = models.ForeignKey(GpsLocation, on_delete=models.SET_NULL, null=True, blank=True)

    objects = RepairManager()

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("repairs:repair_order_detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-timestamp", "-publish"]

    def get_markdown(self):
        content = self.problem_found
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    def get_api_url(self, request=None):
        return api_reverse("api-repairs:repair_order-rud",  kwargs={'slug': self.slug}, request=request)

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


def create_slug_order(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = RepairOrder.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug_order(instance, new_slug=new_slug)
    return slug


def pre_save_repairorder_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug_order(instance)

    if instance.content:
        html_string = instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var


pre_save.connect(pre_save_repairorder_receiver, sender=RepairOrder)


class RepairFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Name of Task or Repair', max_length=250)
    slug = models.SlugField(null=True, blank=True, unique=True, help_text='leave blank or your-brand-name')

    # service provider
    service_provider = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    date_of_invoice = models.DateTimeField(null=True, blank=True)

    # estimate
    estimate_number = models.CharField(max_length=15, null=True, blank=True)
    quoted_price = models.CharField(max_length=5, null=True, blank=True)

    # invoice info
    invoice_number = models.CharField(max_length=10, blank=True, null=True)
    work_order = models.CharField(max_length=10, blank=True, null=True, help_text='work order number' )
    odometer = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, help_text='odometer actual reading')
    tax_id = models.CharField(max_length=20, null=True, blank=True)
    return_parts = models.BooleanField(default=False)
    due_price = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    price_paid = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    # asset info
    asset = models.ForeignKey(TypeOfAsset, on_delete=models.SET_NULL, null=True, blank=True)
    engine = models.ForeignKey(Engines, on_delete=models.SET_NULL, null=True, blank=True)

    # Description of Work
    content = models.TextField('Maintenance/Service Performed', help_text='order detail', blank=True, null=True)
    part_no = models.CharField(max_length=20, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0, blank=True, null=True)
    update = models.DateTimeField(auto_now=True)
    labor_costs = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    # image
    image = models.ImageField(upload_to=upload_location, null=True, blank=True, width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0, null=True)
    width_field = models.IntegerField(default=0, null=True)

    objects = RepairManager()

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("repairs:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-timestamp", "-update"]

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    def get_api_url(self, request=None):
        return api_reverse("api-repairs:repair-rud",  kwargs={'slug': self.slug}, request=request)

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
    qs = RepairFile.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_repair_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.content:
        html_string = instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var


pre_save.connect(pre_save_repair_receiver, sender=RepairFile)
