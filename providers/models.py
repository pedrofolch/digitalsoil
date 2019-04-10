import datetime
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.contrib.gis.db import models as gismodels

from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.utils import timezone
from rest_framework.reverse import reverse as api_reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from .utils import unique_slug_generator, get_read_time
from markdown_deux import markdown
from comments.models import Comment
from shops.models import Shop


User = settings.AUTH_USER_MODEL


class SupplierQuerySet(models.query.QuerySet):

    # def published(self):
    #     return self.filter(publish__lte=timezone.now())

    def search(self, query):
        if query:
            query = query.strip()
            return self.filter(
                Q(id__iexact=query) |
                Q(sprout_name__icontains=query) |
                Q(sprout_name__iexact=query) |
                Q(name_of_supplier__icontains=query) |
                Q(name_of_supplier__iexact=query) |
                Q(name_of_store__icontains=query) |
                Q(name_of_store__iexact=query) |
                Q(phone__icontains=query) |
                Q(phone__iexact=query) |
                Q(address__icontains=query) |
                Q(address__iexact=query) |
                Q(county__icontains=query) |
                Q(county__iexact=query) |
                Q(city__icontains=query) |
                Q(city__iexact=query) |
                Q(state__iexact=query) |
                Q(state__icontains=query) |
                Q(user__iexact=query) |
                Q(user__icontains=query) |
                Q(strain__icontains=query) |
                Q(strain__iexact=query) |
                Q(supplier__icontains=query) |
                Q(supplier__iexact=query)
            ).distinct()
        return self


class SupplierManager(models.Manager):
    def get_queryset(self):
        return SupplierQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)

    # def active(self, *args, **kwargs):
    #     return super(SupplierManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    # filebase, extension = filename.split(".")
    # return "%s/%s.%s" %(instance.id, instance.id, extension)
    supplier_model = instance.__class__
    new_id = supplier_model.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Grow. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


CATEGORY_SUPPLIER = (
    ('CO', 'consumables'),
    ('PE', 'perishables'),
    ('SE', 'service provider'),
    ('ME', 'merchandise'),
    ('SM', 'service & merchandise'),
    ('ED', 'digital services'),
    ('SA', 'sustainable agriculture'),
    ('IN', 'insurance')
)


class Supplies(Shop):
    customers = models.ManyToManyField(Shop, related_name='provider')

    class Meta:
        verbose_name = 'Supply'
        verbose_name_plural = "Supplies"


class Supplier(models.Model):
    title = models.CharField(max_length=60, null=True, blank=True, help_text="Commercial Name")
    contact = models.CharField(max_length=60, null=True, blank=True, help_text="store contact")
    content = models.TextField(null=True, help_text='provider or supplier of what?')
    slug = models.SlugField(null=True, blank=True, unique=True)
    url = models.URLField(null=True, blank=True, help_text='website')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    address = models.OneToOneField(Shop, on_delete=models.SET_NULL, null=True, parent_link=True)
    merchant_category = models.CharField(choices=CATEGORY_SUPPLIER, default='service & merchandise', max_length=2)

    objects = SupplierManager

    class Meta:
        ordering = ['merchant_category', 'address', 'title', 'contact', '-update']

    def __str__(self):
        return str(self.title)

    @property
    def owner(self):
        return self.user

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

    def get_absolute_url(self):
        return reverse('providers:detail', kwargs={'slug': self.slug})

    def was_published_recently(self):
        return self.timestamp >= timezone.now() - datetime.timedelta(days=1)

    def get_api_url(self, request=None):
        return api_reverse("api-providers:supplier-rud", kwargs={'pk': self.pk}, request=request)


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Supplier.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_supplier_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.content:
        html_string = instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var


pre_save.connect(pre_save_supplier_receiver, sender=Supplier)


def rl_supplier_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        instance.save()


post_save.connect(rl_supplier_save_receiver, sender=Supplier)



