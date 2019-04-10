from .utils import get_read_time
from django.db.models.signals import pre_save, post_save
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from rest_framework.reverse import reverse as api_reverse
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db import models

from django.db.models import Q
from markdown_deux import markdown
from comments.models import Comment
from providers.models import Supplier
from .utils import get_read_time, unique_slug_generator


class ProductQuerySet(models.QuerySet):
    def availability(self, *args, **kwargs):
        return self.filter(availability=True)

    def not_draft(self):
        return self.filter(draft=False)

    def published(self):
        return self.filter(publish__lte=timezone.now()).not_draft()

    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                    Q(title__icontains=query) |
                    Q(content__icontains=query) |
                    Q(price__icontains=query) |
                    Q(pim__icontains=query) |
                    Q(supplier__icontains=query) |
                    Q(slug__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def active(self, *args, **kwargs):
        # Post.objects.all() = super(PostManager, self).all()
        return self.get_queryset().published()

    # def in_stock(self, *args, **kwargs):
    #     return self.get_queryset().filter(in_stock=True)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


def upload_location(instance, filename):
    # filebase, extension = filename.split(".")
    # return "%s/%s.%s" %(instance.id, instance.id, extension)
    product_model = instance.__class__
    new_id = product_model.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Grow. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


CATEGORY_CHOICES = (
    ('AG', 'Agriculture'),
    ('M', 'Merchandise'),
    ('A', 'Asset'),
    ('S', 'service'),
    ('O', 'other'),
    ('B', 'bath & body'),
    ('AM', 'auto'),
    ('H', 'heavy equipment'),
    ('MA', 'marine'),
    ('AC', 'air')
)


class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, null=True, on_delete=models.SET_NULL)
    category = models.CharField(choices=CATEGORY_CHOICES, default='B&B', max_length=2)
    sub_category = models.CharField(max_length=25, blank=True, null=True)
    title = models.CharField(max_length=120, help_text='name of the product')
    slug = models.SlugField(null=True, blank=True, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    quantity = models.IntegerField(default=1)
    pim = models.CharField('product information management', max_length=20, default='SRL099138', help_text='serial')
    in_stock = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)

    image = models.ImageField(upload_to=upload_location, null=True, blank=True, width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()

    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)

    read_time = models.IntegerField(default=0)  # models.TimeField(null=True, blank=True) #assume minutes
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    objects = ProductManager()

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-publish", "-updated"]

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    def get_api_url(self, request=None):
        return api_reverse("api-products:product-rud", kwargs={'pk': self.pk}, request=request)

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
    qs = Product.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.content:
        html_string = instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var


pre_save.connect(pre_save_product_receiver, sender=Product)


def rl_post_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        instance.save()


post_save.connect(rl_post_save_receiver, sender=Product)