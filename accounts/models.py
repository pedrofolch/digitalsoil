from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.db.models import Q
from django.core.mail import send_mail
from django.urls import reverse
from .utils import code_generator
from django.utils import timezone

from products.models import Product
import stripe


User = settings.AUTH_USER_MODEL


stripe.api_key = settings.STRIPE_SECRET_KEY


class ProfileQuerySet(models.QuerySet):
    def not_draft(self):
        return self.filter(draft=False)

    def published(self):
        return self.filter(publish__lte=timezone.now()).not_draft()

    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                    Q(first_name__icontains=query) |
                    Q(last_name__icontains=query) |
                    Q(followers__icontains=query)
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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ebooks = models.ManyToManyField(Product, blank=True)
    stripe_id = models.CharField(max_length=200, null=True, blank=True)
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

    def get_absolute_url(self):
        return reverse("accounts:profile", kwargs={"pk": self.pk})


def post_save_profile_create(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

    user_profile, created = Profile.objects.get_or_create(user=instance)

    if user_profile.stripe_id is None or user_profile.stripe_id == '':
        new_stripe_id = stripe.Customer.create(email=instance.email)
        user_profile.stripe_id = new_stripe_id['id']
        user_profile.save()


post_save.connect(post_save_profile_create, sender=settings.AUTH_USER_MODEL)


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
