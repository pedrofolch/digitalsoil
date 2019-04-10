from django.conf import settings

from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.db.models import Q

from django.core.mail import send_mail, EmailMultiAlternatives
from django.urls import reverse
from .utils import code_generator
# from django.core.validators import RegexValidator

# USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$/'

User = settings.AUTH_USER_MODEL

# Create your models here.


class ProfileQuerySet(models.QuerySet):
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
                    Q(slug__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs


class ProfileManager(models.Manager):
    def toggle_follow(self, request_user, username_to_toggle):
        profile_ = Profile.objects.get(user__username__iexact=username_to_toggle)
        user = request_user
        is_following = False
        if user in profile_.followers.all():
            profile_.followers.remove(user)
        else:
            profile_.followers.add(user)
            is_following = True
        return profile_, is_following

    def get_queryset(self):
        return ProfileQuerySet(self.model, using=self._db)

    def active(self, *args, **kwargs):
        # Post.objects.all() = super(PostManager, self).all()
        return self.get_queryset().published()

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class Profile(models.Model):
    # username = models.CharField(
    #     max_length=255,
    #     validators=[RegexValidator(regex=USERNAME_REGEX,
    #     message='Username must be Alpahnumeric or contain any of the following: ". @ + -" ',
    #     code='invalid_username')],
    #     unique=True,)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)  # user.profile
    stripe_id = models.CharField(max_length=300)
    first_name = models.CharField(max_length=35, null=False, default="first name")
    last_name = models.CharField(max_length=35, null=False, default="first name")
    phone_number = models.CharField(max_length=11, blank=True)
    followers = models.ManyToManyField(User, related_name='is_following', blank=True)  # user.is_following.all()
    # following = models.ManyToManyField(User, related_name='following', blank=True) # user.following.all()
    activation_key = models.CharField(max_length=120, blank=True, null=True)
    activated = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ProfileManager()

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user.username

    def send_activation_email(self):
        if not self.activated:
            self.activation_key = code_generator()  # 'somekey' #gen key
            self.save()
            # path_ = reverse()
            path_ = reverse('activate', kwargs={"code": self.activation_key})
            full_path = "https://digitalsoil.herokuapp.com" + path_
            subject = 'Activate Account'
            from_email = settings.DEFAULT_FROM_EMAIL
            message = f'Activate your account here: {full_path}'
            recipient_list = [self.user.email]
            html_message = f'<p>Activate your account here: {full_path}</p>'
            print(html_message)
            sent_mail = send_mail(subject, message, from_email,
                                  recipient_list,
                                  fail_silently=False,
                                  html_message=html_message)
            sent_mail = True
            return sent_mail


def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        profile, is_created = Profile.objects.get_or_create(user=instance)
        default_user_profile = Profile.objects.get_or_create(user__id=1)[0]  # user__username=
        default_user_profile.followers.add(instance)
        # profile.followers.add(default_user_profile.user)
        # profile.followers.add(2)


post_save.connect(post_save_user_receiver, sender=User)


class ActivationProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    key = models.CharField(max_length=120)
    expired = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.key = code_generator()
        super(ActivationProfile, self).save(*args, **kwargs)


def post_save_activation_receiver(sender, instance, created, *args, **kwargs):
    if created:
        # send_email
        print('activation created')


post_save.connect(post_save_activation_receiver, sender=ActivationProfile)


def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
            ActivationProfile.objects.create(user=instance)
        except:
            pass


post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)


class AddressQuerySet(models.QuerySet):
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
                    Q(slug__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs


class AddressManager(models.Manager):
    def toggle_follow(self, request_user, username_to_toggle):
        profile_ = Profile.objects.get(user__username__iexact=username_to_toggle)
        user = request_user
        is_following = False
        if user in profile_.followers.all():
            profile_.followers.remove(user)
        else:
            profile_.followers.add(user)
            is_following = True
        return profile_, is_following

    def get_queryset(self):
        return AddressQuerySet(self.model, using=self._db)

    def active(self, *args, **kwargs):
        # Post.objects.all() = super(PostManager, self).all()
        return self.get_queryset().published()

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class Address(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField('nickname', max_length=120, null=True, blank=True)
    address1 = models.CharField(max_length=300)
    address2 = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=300)
    state = models.CharField(max_length=300)
    country = models.CharField(max_length=300)
    postal_code = models.CharField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now_add=False, auto_now=True)
    default_address = models.BooleanField(default=False)
    billing_address = models.BooleanField(default=False)
    shipping_address = models.BooleanField(default=True)

    objects = AddressManager()

    def __str__(self):
        return self.address1
