import datetime
from django.utils import timezone
from django.core.validators import validate_comma_separated_integer_list
from django.db.models.signals import post_save, pre_save
from django.contrib.contenttypes.models import ContentType

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.db.models import Q
from rest_framework.reverse import reverse as api_reverse
from recipes.models import Recipe
from providers.models import Supplier
from django.utils.safestring import mark_safe

from markdown_deux import markdown
from comments.models import Comment
from .utils import get_read_time, unique_slug_generator
from django.utils.text import slugify


User = settings.AUTH_USER_MODEL


class FieldDataQuerySet(models.query.QuerySet):
    def not_draft(self):
        return self.filter(draft=False)

    def published(self):
        return self.filter(publish__lte=timezone.now().not_draft())

    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                    Q(title__icontains=query) |
                    Q(title__iexact=query) |
                    Q(slug__iexact=query) |
                    Q(brand_name__icontains=query) |
                    Q(pile_name__icontains=query) |
                    Q(pile_name__iexact=query) |
                    Q(new_pile_name__iexact=query)
            ).distinct()
            qs = qs.filter(or_lookup).distinct()
        return qs


class FieldDataManager(models.Manager):
    def get_queryset(self):
        return FieldDataQuerySet(self.model, using=self._db)

    def active(self, *args, **kwargs):
        # FieldData.objects.all() = super(FieldDataManager, self).all()
        return self.get_queryset().published()

    def search(self, query=None):
        return self.get_queryset().search(query=query)


def upload_location(instance, filename):
    field_data_model = instance.__class__
    new_id = field_data_model.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


class FieldData(models.Model):
    title = models.CharField('task name', max_length=120)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    brand_name = models.ForeignKey(Supplier, null=True, on_delete=models.SET_NULL)
    pile_name = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(null=True, blank=True, unique=True, help_text='leave blank or your-brand-name')
    merge_into_pile = models.BooleanField(default=False)
    merge_with_pile = models.CharField(max_length=20, blank=True, null=True)
    new_pile_name = models.CharField(max_length=120, help_text='only if mixing piles', blank=True, null=True)

    created = models.DateTimeField('date created', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(auto_now=True, auto_now_add=False)

    image = models.ImageField(upload_to=upload_location, null=True, blank=True, width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()

    timestamp = models.DateTimeField(auto_now=True)
    days = models.IntegerField('days since turned', default=0)

    # triggers and conditions
    must_turn_pile = models.BooleanField(default=False)
    must_water_now = models.BooleanField(default=False)
    is_pile_ready = models.BooleanField(default=False)
    turn_cycle = models.IntegerField(default=0)
    times_watered = models.IntegerField(default=0)

    # actions taken
    turned = models.BooleanField(default=False)
    watered = models.BooleanField(default=False)

    MEASURED_USING_CHOICE = (
        ('O', 'observation'),
        ('D', 'device'),
        ('T', 'thermometer')
    )

    humidity_measured_with = models.CharField(choices=MEASURED_USING_CHOICE, max_length=1)
    temperature_measured_with = models.CharField(choices=MEASURED_USING_CHOICE, max_length=1)
    celsius = models.BooleanField(default=False)

    # Metrics on Pile
    core_temperature_readings = models.CharField(validators=[validate_comma_separated_integer_list],
                                                 max_length=255,
                                                 blank=True,
                                                 null=True,
                                                 help_text='comma separated temperature measurements, no white space'
                                                 )
    core_humidity_readings = models.CharField(validators=[validate_comma_separated_integer_list],
                                              max_length=155,
                                              blank=True,
                                              null=True,
                                              help_text='comma separated humidity measurements, no white space')

    # Averages
    average_temperature = models.IntegerField(null=True, blank=True)
    average_humidity = models.IntegerField(null=True, blank=True)

    objects = FieldDataManager()

    def __str__(self):
        return '%s - Brand: %s, last worked on: %s' % (self.title,
                                                       self.brand_name,
                                                       self.timestamp
                                                       )

    def get_absolute_url(self):
        return reverse("fieldwork:average", kwargs={'slug': self.slug})

    class Meta:
        ordering = ['user', "-timestamp", 'created']
        verbose_name = 'field data'
        verbose_name_plural = 'fields data'

    def get_api_url(self, request=None):
        return api_reverse("api-fieldwork:field-rud", kwargs={'pk': self.pk}, request=request)

    def was_created_recently(self):
        return self.created >= timezone.now() - datetime.timedelta(days=1)

    def was_updated_recently(self):
        return self.updated >= timezone.now() - datetime.timedelta(days=1)

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def owner(self):
        return self.user

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    # def water_status(self):
    #     instance = self
    #     times_watered = FieldData.objects.all(instance)
    #     if 70 <= times_watered[0].average_temperature and times_watered[0].days >= 7:
    #         times_watered[0].is_pile_ready = True
    #         print(times_watered[0].is_pile_ready)
    #         times_watered[0].save()
    #         return super(times_watered)
    #
    #     elif 131 >= times_watered[0].average_temperature <= 140 and times_watered[0].days >= 3:
    #         times_watered[0].must_turn_pile = True
    #         print(times_watered[0].average_temperature, times_watered[0].must_turn_pile)
    #         if times_watered[0].turned:
    #             times_watered[0].days = 0
    #             times_watered[0].turn_cycle += 1
    #             times_watered[0].save()
    #             print(times_watered[0].days)
    #             print(times_watered[0].turned)
    #             print(times_watered[0].must_turn_pile)
    #             return super(times_watered)
    #
    #     elif 141 >= times_watered[0].average_temperature <= 150 and times_watered[0][0].days >= 2:
    #         times_watered[0].must_turn_pile = True
    #         print(times_watered[0].average_temperature, times_watered[0].must_turn_pile)
    #         if times_watered[0].turned:
    #             times_watered[0].turn_cycle += 1
    #             times_watered[0].days = 0
    #             times_watered[0].save()
    #             print(times_watered[0].days)
    #             print(times_watered[0].turn_cycle)
    #             return super(times_watered)
    #
    #     elif 151 >= times_watered[0].average_temperature <= 160 and times_watered[0].days >= 1:
    #         must_turn_pile = True
    #         print(times_watered[0].average_temperature, must_turn_pile)
    #
    #         if times_watered[0].turned:
    #             times_watered[0].days = 0
    #             times_watered[0].turn_cycle += 1
    #             times_watered[0].save()
    #             print(times_watered[0].days)
    #             print(times_watered[0].turn_cycle)
    #             return super(times_watered)
    #
    #     elif times_watered[0].average_temperature >= 161:
    #         times_watered[0].must_turn_pile = True
    #         print(times_watered[0].average_temperature, times_watered[0].must_turn_pile)
    #         if times_watered[0].turned:
    #             times_watered[0].days = 0
    #             times_watered[0].turn_cycle += 1
    #             times_watered[0].save()
    #             print(times_watered[0].days)
    #             print(times_watered[0].turn_cycle)
    #             return super(times_watered)
    #
    #     if times_watered[0].turned:
    #         times_watered[0].turn_cycle += 1
    #         print(times_watered[0].turn_cycle)
    #         times_watered[0].save()
    #         return super(times_watered)
    #     else:
    #         pass
    #
    #     if times_watered[0].watered:
    #         times_watered[0].times_watered += 1
    #         print(times_watered[0].times_watered)
    #         times_watered[0].save()
    #         return super(times_watered)
    #     else:
    #         pass
    #     print(times_watered[0].days)
    #     print(times_watered[0].turn_cycle)
    #     print(times_watered[0].is_pile_ready)
    #     print(times_watered[0].must_turn_pile)
    #     print(times_watered[0].must_water_now)
    #     times_watered.save()
    #
    #     if times_watered[0].average_humidity < 45:
    #         times_watered[0].must_water_now = True
    #         times_watered[0].save()
    #         print(times_watered[0].must_water_now)
    #     return super(times_watered)


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = FieldData.objects.filter(slug=slug).order_by("-id")
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


pre_save.connect(pre_save_post_receiver, sender=FieldData)


def rl_post_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        instance.save()


post_save.connect(rl_post_save_receiver, sender=FieldData)
