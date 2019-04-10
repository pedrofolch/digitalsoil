
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from rest_framework.reverse import reverse as api_reverse
from django.core.validators import validate_comma_separated_integer_list


from markdown_deux import markdown
from comments.models import Comment
from recipes.models import Recipe

from .utils import get_read_time, unique_slug_generator

User = settings.AUTH_USER_MODEL


# Create your models here.
MAGNIFYING_CHOICE = (
    ('2038', '18 x 18'),
    ('2491', '22 x 18'),
    ('3044', '22 x 22')
)


EXPECTED_RANGE_CHOICE = (
    ('UN', 'unknown'),
    ('3-3', '300 - 3000'),
    ('3-12', '3 - 12'),
    ('1-200', '100 - 2000')
)

DEAD_LIVE_CHOICE = (
    ('D', 'dead'),
    ('A', 'alive'),
    ('UN', 'unknown')
)

VIEW_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
    ('13', '13'),
    ('14', '14'),
    ('15', '15'),
    ('16', '16'),
    ('17', '17'),
    ('18', '18'),
    ('19', '19'),
    ('20', '20'),

)


class LabManager(models.Manager):
    def active(self, *args, **kwargs):
        # Lab.objects.all() = super(LabManager, self).all()
        return super(LabManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object,
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """

    filebase, extension = filename.split(".")
    # return "%s/%s.%s" %(instance.id, instance.id, extension)
    microscope_view_model = instance.__class__
    new_id = microscope_view_model.objects.order_by("id").last().id + 1
    print(filebase)

    return "%s/%s" % (new_id, filename)


class Lab(models.Model):
    """
    lab soil sample analytics for Compost Piles, each view equals to each step of the analytical observations
    images are describe in each view
    """
    # observed_by is the user or observer
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, null=True, on_delete=models.SET_NULL)
    # find organisms
    title = models.CharField(max_length=120, default='Bio-Assesment')
    slug = models.SlugField(null=True, blank=True, unique=True, help_text='leave blank or your-brand-name')
    sample_id = models.CharField(max_length=60)
    # Name of the Client or Title of the Job and reference
    pile_name = models.ForeignKey(Recipe, null=True, on_delete=models.SET_NULL)

    # dates and information
    collected_by = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_collected = models.DateField(auto_now=False, auto_now_add=False, help_text='yyyy/mm/dd')
    date_observed = models.DateField(auto_now=False, blank=True, help_text='yyyy/mm/dd')

    coverlip_size = models.CharField(max_length=120, choices=MAGNIFYING_CHOICE, default='2038')
    number_of_drops_placed = models.DecimalField(max_digits=8, decimal_places=0, default=2)
    drops_per_ml = models.DecimalField(max_digits=8, decimal_places=3, default=0.00)

    # Nematodes
    nematodes_bacterial_feeders = models.PositiveIntegerField(default=0)
    nematodes_fungal_feeders = models.PositiveIntegerField(default=0)
    nematodes_predatory = models.PositiveIntegerField(default=0)
    nematodes_switchers = models.PositiveIntegerField(default=0)
    nematodes_root_feeders = models.PositiveIntegerField(default=0)
    nematodes_omnivores = models.PositiveIntegerField(default=0)
    total_nematodes = models.PositiveIntegerField(default=0)
    total_beneficial = models.PositiveIntegerField(default=0)
    total_detrimentals = models.PositiveIntegerField(default=0)

    # dilution should be from 5 to 2000 in increments of 5
    nematodes_total_num_p_gram = models.DecimalField(max_digits=8, decimal_places=3, default=0.00)
    nematodes_dilution = models.DecimalField(max_digits=8, decimal_places=3, default=5,
                                             help_text='in multiple of 5, up to 2000')
    nematodes_expected_range = models.CharField(choices=EXPECTED_RANGE_CHOICE, max_length=5, default='1-200')
    comments_nematodes = models.TextField('comments on nematodes', blank=True)

    # organisms
    ciliates = models.CharField(validators=[validate_comma_separated_integer_list],
                                max_length=300,
                                blank=True,
                                null=True,
                                help_text='comma separated, no white space'
                                )
    ciliates_mean = models.DecimalField(max_digits=9, decimal_places=3, default=0.00)

    flagellates = models.CharField(validators=[validate_comma_separated_integer_list], max_length=300,
                                   blank=True, null=True,
                                   help_text='comma separated, no white space')
    flagellates_mean = models.DecimalField(max_digits=9, decimal_places=3, default=0.00)

    amoeba = models.CharField(validators=[validate_comma_separated_integer_list],
                              max_length=300,
                              blank=True,
                              null=True,
                              help_text='comma separated, no white space'
                              )
    amoeba_mean = models.DecimalField(max_digits=9, decimal_places=3, default=0.00)

    oomycetes = models.CharField(max_length=300, blank=True, null=True, help_text='comma separated')

    oomycetes_mean = models.DecimalField(max_digits=9, decimal_places=3, default=0.00)

    oomy_diameter = models.CharField(max_length=300, blank=True, default=0,
                                      help_text='comma separated'
                                     )
    oomy_diameter_mean = models.DecimalField(max_digits=9, decimal_places=3, default=0.00)

    oomy_color = models.CharField(max_length=380, default='none')

    fungi = models.CharField(max_length=380, blank=True, null=True, help_text='comma separated')

    fungi_mean = models.DecimalField(max_digits=9, decimal_places=3, default=0.00)
    fungi_diameter = models.CharField(max_length=300, blank=True, default=0, help_text='comma separated')
    fungi_diameter_mean = models.DecimalField(max_digits=9, decimal_places=3, default=0.00)
    fungi_color = models.CharField(max_length=380, default='none')

    actinobacteria = models.CharField(max_length=300, blank=True, null=True, help_text='comma separated')

    actinobacteria_mean = models.DecimalField(max_digits=9, decimal_places=3, default=0.00)

    bacteria = models.CharField(max_length=300, blank=True, null=True, help_text='comma separated')

    bacteria_mean = models.DecimalField(max_digits=9, decimal_places=3, default=0.00)

    # Fields and views
    # field_view = models.CharField(choices=VIEW_CHOICES, max_length=2, default=1)
    ciliates_total_mg_per_g = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    ciliates_dilution = models.DecimalField(max_digits=9, decimal_places=0, default=5, help_text='integers of 5')
    comments_ciliates = models.TextField('comments', blank=True)
    ciliates_expected_range = models.CharField(choices=EXPECTED_RANGE_CHOICE, max_length=5, default='3-3')
    ciliates_st_diviation = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    actinobacteria_total_mg_per_g = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    actinobacteria_dilution = models.PositiveIntegerField(default=5)

    comments_actinobacteria = models.TextField('comments', blank=True)
    actinobacteria_expected_range = models.CharField(choices=EXPECTED_RANGE_CHOICE, max_length=5, default='3-3')
    actinobacteria_st_diviation = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    oomycetes_total_mg_per_g = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    oomycetes_dilution = models.PositiveIntegerField(default=5)
    comments_oomycetes = models.TextField('comments', blank=True)
    oomycetes_expected_range = models.CharField(choices=EXPECTED_RANGE_CHOICE, max_length=5, default='3-3')
    oomycetes_st_diviation = models.DecimalField(max_digits=7, decimal_places=3, default=0.000)

    fungi_total_mg_per_g = models.DecimalField(max_digits=9, decimal_places=3, default=0.000)
    fungi_dilution = models.PositiveIntegerField(default=5)
    comments_fungi = models.TextField('comments', blank=True)
    fungi_expected_range = models.CharField(choices=EXPECTED_RANGE_CHOICE, max_length=5, default='3-3')
    fungi_st_diviation = models.DecimalField(max_digits=7, decimal_places=3, default=0.000)

    # esto es el promedio del diametro del fungi
    de_av_hyphal_dia = models.DecimalField(max_digits=6, decimal_places=3, default=0.000)
    comments_de_av_hyphal_dia = models.TextField(blank=True)
    de_av_hyphal_dia_expected_range = models.CharField(max_length=5, choices=EXPECTED_RANGE_CHOICE, default="3-12")
    de_av_hyphal_dia_mean = models.DecimalField(max_digits=6, decimal_places=3, default=0.000)

    bacteria_total_mg_per_g = models.DecimalField(max_digits=9, decimal_places=3, default=0.000)
    bacteria_dilution = models.PositiveIntegerField(default=5)
    bacteria_expected_range = models.CharField(choices=EXPECTED_RANGE_CHOICE, max_length=5, default='3-3')
    bacteria_st_diviation = models.DecimalField(max_digits=7, decimal_places=3, default=0.000)
    comments_bacteria = models.TextField('comments', blank=True)

    bn_av_hyphal_dia = models.DecimalField(max_digits=6, decimal_places=3, default=0.000)
    comments_bn_av_hyphal_dia = models.TextField(blank=True)
    bn_av_hyphal_dia_expected_range = models.CharField(max_length=5, choices=EXPECTED_RANGE_CHOICE, default="3-12")
    bn_av_hyphal_dia_mean = models.DecimalField(max_digits=6, decimal_places=3, default=0.000)

    flagellates_total_mg_per_g = models.DecimalField(max_digits=9, decimal_places=3, default=0.000)
    flagellates_dilution = models.PositiveIntegerField(default=5)
    comments_flagellates = models.TextField('comments', blank=True)
    flagellates_expected_range = models.CharField(choices=EXPECTED_RANGE_CHOICE, max_length=5, default='3-3')
    flagellates_st_diviation = models.DecimalField(max_digits=7, decimal_places=3, default=0.000)

    amoeba_total_mg_per_g = models.DecimalField(max_digits=9, decimal_places=3, default=0.000)
    amoeba_dilution = models.PositiveIntegerField(default=5)
    comments_amoeba = models.TextField('comments', blank=True)
    amoeba_expected_range = models.CharField(choices=EXPECTED_RANGE_CHOICE, max_length=5, default='3-3')
    amoeba_st_diviation = models.DecimalField(max_digits=7, decimal_places=3, default=0.000)

    # Shapes
    cocci = models.BooleanField(default=False)
    cocci_chains = models.BooleanField(default=False)
    bacillus = models.BooleanField(default=False)
    bacili_chains = models.BooleanField(default=False)
    cocobacili = models.BooleanField(default=False)
    spirochetes = models.BooleanField(default=False)
    spirilla = models.BooleanField(default=False)

    comments_hyphal = models.TextField('hyphal comments', blank=True)

    # aggregates
    aggregates_humics = models.TextField(blank=True)
    comments_humics = models.TextField('humics comments', blank=True)

    aggregates_fulvics = models.TextField(blank=True)
    comments_fulvics = models.TextField('fulvics comments', blank=True)

    # other organisms
    earthworms = models.CharField(choices=DEAD_LIVE_CHOICE, max_length=2, default="UN")
    comments_earthworms = models.TextField('earthworms comments', blank=True)

    insect_larvae = models.CharField(choices=DEAD_LIVE_CHOICE, max_length=2, default="UN")
    comments_insect_larvae = models.TextField('insect larvae comments', blank=True)

    microarthropods = models.CharField(choices=DEAD_LIVE_CHOICE, max_length=2, default="UN")
    comments_microarthropods = models.TextField('microarthropods comments', blank=True)

    rotifers = models.CharField(choices=DEAD_LIVE_CHOICE, max_length=2, default="UN")
    comments_rotifers = models.TextField('rotifer comments', blank=True)

    # image and content
    image = models.ImageField(upload_to=upload_location, null=True, blank=True, width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField(blank=True)
    read_time = models.IntegerField(default=0)  # models.TimeField(null=True, blank=True) #assume minutes

    video_url = models.CharField(max_length=200)

    # publish & draft
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    comments_general = models.TextField('comments', blank=True)
    other_notes = models.TextField(blank=True)

    objects = LabManager()

    def __str__(self):
        return str(self.sample_id)

    @property
    def owner(self):
        return self.user

    def get_api_url(self, request=None):
        return api_reverse("api-labsoil:lab-rud",  kwargs={'pk': self.pk}, request=request)

    def get_absolute_url(self):
        return reverse("labsoil:result", kwargs={'slug': self.slug})

    class Meta:
        ordering = ["-timestamp", "-updated"]

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
    qs = Lab.objects.filter(slug=slug).order_by("-id")
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


pre_save.connect(pre_save_post_receiver, sender=Lab)


def rl_post_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        instance.save()


post_save.connect(rl_post_save_receiver, sender=Lab)
