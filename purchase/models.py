
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from rest_framework.reverse import reverse as api_reverse

from markdown_deux import markdown
from comments.models import Comment

from .utils import get_read_time, unique_slug_generator
from providers.models import Supplier, Supplies
from assets.models import TypeOfAsset
from engine_room.models import Engines

# Create your models here.


class PurchaseOrder(models.Model):
    # Name of what is wanted or needed
    title = models.CharField(max_length=100, help_text='Command Order')
    slug = models.SlugField(null=True, blank=True, unique=True)
    order_number = models.PositiveIntegerField(default=0)
    purchase_number = models.CharField(max_length=25, unique=True)

    # date
    date_ordered = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    # Provider
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    item = models.CharField(max_length=100, null=True, blank=True)
    product_number = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)

    # Price & Shipping Cost
    cost_of_item = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    # ordered by
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             default=1,
                             null=True,
                             on_delete=models.SET_NULL,
                             help_text='ordered by')

    # Related to
    for_asset = models.ForeignKey(TypeOfAsset, on_delete=models.SET_NULL, null=True, blank=True)
    for_engine = models.ForeignKey(Engines, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.title)

    @property
    def owner(self):
        return self.user

    def get_api_url(self, request=None):
        return api_reverse("api-purchase:po-rud",  kwargs={'pk': self.pk}, request=request)

    def get_absolute_url(self):
        return reverse("purchase:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-timestamp", "-date_ordered"]

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

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


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = PurchaseOrder.objects.filter(slug=slug).order_by("-id")
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


pre_save.connect(pre_save_post_receiver, sender=PurchaseOrder)


def rl_post_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        instance.save()


post_save.connect(rl_post_save_receiver, sender=PurchaseOrder)
