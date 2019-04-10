import datetime
from django.contrib.contenttypes.models import ContentType

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.utils import timezone
from rest_framework.reverse import reverse as api_reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from providers.models import Supplier
from .utils import unique_slug_generator
from markdown_deux import markdown
from comments.models import Comment


class RecipeQuerySet(models.QuerySet):
    def not_public(self):
        return self.filter(public=False)

    def not_draft(self):
        return self.filter(draft=False)

    def published(self):
        return self.filter(publish__lte=timezone.now().not_draft())

    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                    Q(pile_name__icontains=query) |
                    Q(pile_name__iexact=query) |
                    Q(supplier__icontains=query) |
                    Q(supplier__iexact=query) |
                    Q(slug__icontains=query) |
                    Q(slug__iexact=query) |
                    Q(username__iexact=query) |
                    Q(username__icontains=query) |
                    Q(user__icontains=query) |
                    Q(user__iexact=query) |
                    Q(ready_to_use__iexact=query) |
                    Q(category__iexact=query) |
                    Q(category__icontains=query) |
                    Q(observation__icontains=query) |
                    Q(observation__iexact=query) |
                    Q(publish__icontains=query) |
                    Q(publish__iexact=query) |
                    Q(update__icontains=query) |
                    Q(update__iexact=query) |
                    Q(contains__icontains=query) |
                    Q(contains__iexact=query) |
                    Q(public__icontains=query) |
                    Q(public__iexact=query) |
                    Q(category_value__icontains=query) |
                    Q(category_value__iexact=query) |
                    Q(recipe_name__icontains=query) |
                    Q(recipe_name__iexact=query) |
                    Q(nitrogen_material__icontains=query) |
                    Q(nitrogen_material__iexact=query) |
                    Q(type_of_bucket_nitrogen__icontains=query) |
                    Q(type_of_bucket_nitrogen__iexact=query) |
                    Q(amount_nitrogen__icontains=query) |
                    Q(amount_nitrogen__iexact=query) |
                    Q(nitrogen_material_two__icontains=query) |
                    Q(nitrogen_material_two__iexact=query) |
                    Q(type_of_bucket_nitrogen_two__icontains=query) |
                    Q(type_of_bucket_nitrogen_two__iexact=query) |
                    Q(amount_nitrogen_two__icontains=query) |
                    Q(amount_nitrogen_two__iexact=query) |
                    Q(nitrogen_material_three__icontains=query) |
                    Q(nitrogen_material_three__iexact=query) |
                    Q(type_of_bucket_nitrogen_three__icontains=query) |
                    Q(type_of_bucket_nitrogen_three__iexact=query) |
                    Q(amount_nitrogen_three__icontains=query) |
                    Q(amount_nitrogen_three__iexact=query) |
                    Q(high_nitrogen_material__iexact=query) |
                    Q(high_nitrogen_material__icontains=query) |
                    Q(type_of_bucket_high_nitrogen__icontains=query) |
                    Q(type_of_bucket_high_nitrogen__iexact=query) |
                    Q(amount_high_nitrogen__icontains=query) |
                    Q(amount_high_nitrogen__iexact=query) |
                    Q(high_nitrogen_material_two__iexact=query) |
                    Q(high_nitrogen_material_two__icontains=query) |
                    Q(type_of_bucket_high_nitrogen_two__icontains=query) |
                    Q(type_of_bucket_high_nitrogen_two__iexact=query) |
                    Q(amount_high_nitrogen_two__icontains=query) |
                    Q(amount_high_nitrogen_two__iexact=query) |
                    Q(high_nitrogen_material_three__iexact=query) |
                    Q(high_nitrogen_material_three__icontains=query) |
                    Q(type_of_bucket_high_nitrogen_three__icontains=query) |
                    Q(type_of_bucket_high_nitrogen_three__iexact=query) |
                    Q(amount_high_nitrogen_three__icontains=query) |
                    Q(amount_high_nitrogen_three__iexact=query) |
                    Q(carbon_material__iexact=query) |
                    Q(carbon_material__icontains=query) |
                    Q(type_of_bucket_carbon__icontains=query) |
                    Q(type_of_bucket_carbon__iexact=query) |
                    Q(amount_carbon__icontains=query) |
                    Q(amount_carbon__iexact=query) |
                    Q(carbon_material_two__iexact=query) |
                    Q(carbon_material_two__icontains=query) |
                    Q(type_of_bucket_carbon_two__icontains=query) |
                    Q(type_of_bucket_carbon_two__iexact=query) |
                    Q(amount_carbon_two__icontains=query) |
                    Q(amount_carbon_two__iexact=query) |
                    Q(carbon_material_three__iexact=query) |
                    Q(carbon_material_three__icontains=query) |
                    Q(type_of_bucket_carbon_three__icontains=query) |
                    Q(type_of_bucket_carbon_three__iexact=query) |
                    Q(amount_carbon_three__icontains=query) |
                    Q(amount_carbon_three__iexact=query) |
                    Q(wide__iexact=query) |
                    Q(wide__icontains=query) |
                    Q(length__icontains=query) |
                    Q(length__iexact=query) |
                    Q(tall__icontains=query) |
                    Q(tall__iexact=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs


class RecipeManager(models.Manager):
    def get_queryset(self):
        return RecipeQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)


class Category(models.Model):
    category_name = models.CharField("type of compost", max_length=60, null=False, unique=True, default='Bulk')

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["category_name"]

    def __str__(self):
        return str(self.category_name)


def upload_location(instance, filename):
    filebase, extension = filename.split(".")
    # return "%s/%s.%s" %(instance.id, instance.id, extension)
    recipe_model = instance.__class__
    new_id = recipe_model.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object,
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


class Recipe(models.Model):
    # Recipe and Pile information, how does it belong to, name etc.
    producer = models.ForeignKey(Supplier, null=True, on_delete=models.SET_NULL)
    pile_name = models.CharField("pile name", max_length=60, unique=True, null=False,
                                 help_text='make unique, your brand + pile name')
    slug = models.SlugField(null=True, blank=True, unique=True)

    image = models.ImageField(upload_to='upload_location', null=True, blank=True, width_field="width_field",
                              height_field="height_field"
                              )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    content = models.TextField()

    observation = models.CharField(max_length=120, default="none")

    publish = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, verbose_name="worked by",
                             help_text='person in working the pile')
    # is product ready
    ready_to_use = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
    draft = models.BooleanField(default=False)

    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    category_value = models.IntegerField("price for sale", null=False, default=50,
                                         help_text='usefull for commercial use')

    recipe_name = models.CharField(max_length=60, null=False, default="recipe", verbose_name="recipe",
                                   help_text='name of recipe used')

    nitrogen_material = models.CharField("nitrogen material used", max_length=25, default='grass clips')
    type_of_bucket_nitrogen = models.IntegerField('bucket size', null=False, default=2,
                                                  help_text='amount of buckets needed for one cubic yard')
    amount_nitrogen = models.DecimalField("amount of buckets used", max_digits=8, decimal_places=2, default=0)

    nitrogen_material_two = models.CharField("second nitrogen material used", max_length=25, default='none')
    type_of_bucket_nitrogen_two = models.IntegerField('bucket size', null=False, default=0,
                                                      help_text='amount of buckets needed for one cubic yard')
    amount_nitrogen_two = models.DecimalField("amount of buckets used", max_digits=8, decimal_places=2, default=0)

    nitrogen_material_three = models.CharField("third nitrogen material used", max_length=25, default='none')
    type_of_bucket_nitrogen_three = models.IntegerField('bucket size', null=False, default=0,
                                                        help_text='amount of buckets needed for one cubic yard')
    amount_nitrogen_three = models.DecimalField("amount of buckets used", max_digits=8, decimal_places=2, default=0)

    high_nitrogen_material = models.CharField("high nitrogen material used", max_length=25, null=False,
                                              default='manure')
    type_of_bucket_high_nitrogen = models.IntegerField('bucket size', null=False, default=2,
                                                       help_text='amount of buckets needed for one cubic yard')
    amount_high_nitrogen = models.DecimalField("amount of buckets used", max_digits=8, decimal_places=2, default=0)

    high_nitrogen_material_two = models.CharField("second high nitrogen material used", max_length=25,
                                                  null=False, default='none')
    type_of_bucket_high_nitrogen_two = models.IntegerField('bucket size', null=False, default=0,
                                                           help_text='amount of buckets needed for one cubic yard')
    amount_high_nitrogen_two = models.DecimalField("amount of buckets used", max_digits=8, decimal_places=2, default=0)

    high_nitrogen_material_three = models.CharField("third high nitrogen material used", max_length=25,
                                                    null=False, default='none')
    type_of_bucket_high_nitrogen_three = models.IntegerField('bucket size', null=False, default=0)
    amount_high_nitrogen_three = models.DecimalField("amount of buckets used", max_digits=8,
                                                     decimal_places=2, default=0,
                                                     help_text='amount of buckets needed for one cubic yard')

    carbon_material = models.CharField("carbon material used", max_length=25, null=False, default='wood chips')
    type_of_bucket_carbon = models.IntegerField('bucket size', null=False, default=2)
    amount_carbon = models.DecimalField("amount of buckets used", max_digits=8, decimal_places=2, default=0,
                                        help_text='amount of buckets needed for one cubic yard')

    carbon_material_two = models.CharField("Second carbon material used", max_length=25, null=False, default='none')
    type_of_bucket_carbon_two = models.IntegerField('bucket size', null=False, default=0)
    amount_carbon_two = models.DecimalField("amount of buckets used", max_digits=8, decimal_places=2, default=0,
                                            help_text='amount of buckets needed for one cubic yard')

    carbon_material_three = models.CharField("third carbon material used", max_length=25, null=False, default='none')
    type_of_bucket_carbon_three = models.IntegerField('bucket size', null=False, default=0)
    amount_carbon_three = models.DecimalField("amount of buckets used", max_digits=8, decimal_places=2, default=0,
                                              help_text='amount of buckets needed for one cubic yard')

    wide = models.DecimalField("width of designated area", max_digits=8, decimal_places=2, default=0,
                               help_text='in feet')
    length = models.DecimalField("length of designated area", max_digits=8, decimal_places=2, default=0,
                                 help_text='in feet')
    tall = models.DecimalField("height of compost", max_digits=8, decimal_places=2, default=0,
                               help_text='in feet')

    objects = RecipeManager()

    class Meta:
        ordering = ['producer', '-pile_name', '-recipe_name', '-publish', '-update']

    def __str__(self):
        return str(self.pile_name)

    def get_absolute_url(self):
        return reverse("recipes:detail", kwargs={'slug': self.slug})

    def was_published_recently(self):
        return self.publish >= timezone.now() - datetime.timedelta(days=1)

    def get_api_url(self, request=None):
        return api_reverse("api-recipes:pileofcompost-rud", kwargs={'slug': self.slug}, request=request)

    @property
    def title(self):
        return self.recipe_name

    @property
    def owner(self):
        return self.user

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
    qs = Recipe.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


def rl_post_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        instance.save()


pre_save.connect(rl_pre_save_receiver, sender=Recipe)


post_save.connect(rl_post_save_receiver, sender=Recipe)
