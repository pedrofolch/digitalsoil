
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.db.models import Q


from pileofcompost.models import PileOfCompost
from brandnames.models import BrandName


User = settings.AUTH_USER_MODEL


class FieldWorkQuerySet(models.query.QuerySet):
    def search(self, query):
        if query:
            query = query.strip()
            return self.filter(
                Q(worked_by__icontains=query) |
                Q(worked_by__iexact=query) |
                Q(manufacturer__icontains=query) |
                Q(manufacturer__iexact=query) |
                Q(user__icontains=query) |
                Q(user__iexact=query) |
                Q(timestamp__iexact=query) |
                Q(update__iexact=query) |
                Q(city__iexact=query)
                ).distinct()
        return self


class FieldWorkManager(models.Manager):
    def get_queryset(self):
        return FieldWorkQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)


def upload_location(instance, filename):
    # filebase, extension = filename.split(".")
    # return "%s/%s.%s" %(instance.id, instance.id, extension)
    fieldworkmodel = instance.__class__
    new_id = fieldworkmodel.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Grow. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


class FieldWork(models.Model):
    # associations
    worked_by = models.CharField(max_length=35, null=False, default='First Name Last Name')
    working_for = models.ForeignKey(BrandName, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    pile_name = models.ForeignKey(PileOfCompost, null=True, on_delete=models.SET_NULL)
    # item stuff
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    # core_temperature = models.TextField(validators=[validate_comma_separated_integer_list])
    core_temperature = models.TextField(null=True, blank=True, help_text='comma separated field')
    core_humidity = models.TextField(null=True, blank=True, help_text='comma separated field')
    # core_humidity = models.TextField(validators=[validate_comma_separated_integer_list])

    # item stuff
    watered = models.BooleanField(default=False)
    turned = models.BooleanField(default=False)
    turn_cycle = models.IntegerField(default=0)
    # images
    # image = models.ImageField(upload_to='media_cdn/', default='media/',
    #                           null=True,
    #                           blank=True,
    #                           width_field="width_field",
    #                           height_field="height_field")
    # height_field = models.IntegerField(default=0)
    # width_field = models.IntegerField(default=0)

    class Meta:
        ordering = ['-update', '-timestamp', 'pile_name', 'user']

    def __str__(self):
        return self.pile_name

    def get_absolute_url(self):
        return reverse('fieldwork:action', kwargs={'pk': self.pk})

    def get_core_temperature(self):
        return self.core_temperature.split(",")

    def get_core_humidity(self):
        return self.core_humidity.split(",")
