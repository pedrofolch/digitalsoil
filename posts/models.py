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


class PostQuerySet(models.QuerySet):
    def not_draft(self):
        return self.filter(draft=False)

    def published(self):
        return self.filter(publish__lte=timezone.now().not_draft())

    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                    Q(blog__icontains=query) |
                    Q(headline__icontains=query) |
                    Q(title__icontains=query) |
                    Q(content__icontains=query) |
                    Q(authors__icontains=query) |
                    Q(slug__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def active(self, *args, **kwargs):
        # Post.objects.all() = super(PostManager, self).all()
        return self.get_queryset().published()

    def search(self, query=None):
        return self.get_queryset().search(query=query)


"""  # working query 
class PostQuerySet(models.query.QuerySet):
    def not_draft(self):
        return self.filter(draft=False)

    def published(self):
        return self.filter(publish__lte=timezone.now()).not_draft()


class PostManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return PostQuerySet(self.model, using=self._db)

    def active(self, *args, **kwargs):
        # Post.objects.all() = super(PostManager, self).all()
        return self.get_queryset().published()

    """

# old PostManager lets see how the new one works
# class PostManager(models.Manager):
#     def active(self, *args, **kwargs):
#         # Post.objects.all() = super(PostManager, self).all()
#         return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    filebase, extension = filename.split(".")
    # return "%s/%s.%s" %(instance.id, instance.id, extension)
    post_model = instance.__class__
    new_id = post_model.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


class Blog(models.Model):
    # Defines Blog that goes to and tag line topic
    name = models.CharField(max_length=100)
    tag_line = models.TextField()

    def __str__(self):
        return self.name


class Author(models.Model):
    # Author
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Post(models.Model):
    # Post and Image
    blog = models.ForeignKey(Blog, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(null=True, blank=True, unique=True, help_text='leave blank or your-brand-name')
    headline = models.CharField(max_length=255)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True, width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0, null=True)
    width_field = models.IntegerField(default=0, null=True)
    content = models.TextField()

    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=True)
    read_time = models.IntegerField(default=0)  # models.TimeField(null=True, blank=True) #assume minutes
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    authors = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    n_comments = models.IntegerField(default=0)
    n_ping_backs = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)

    objects = PostManager()

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-timestamp", "-updated"]

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    def get_api_url(self, request=None):
        return api_reverse("api-posts:post-rud",  kwargs={'pk': self.pk}, request=request)

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
    qs = Post.objects.filter(slug=slug).order_by("-id")
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


pre_save.connect(pre_save_post_receiver, sender=Post)


def rl_post_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        instance.save()


post_save.connect(rl_post_save_receiver, sender=Post)
