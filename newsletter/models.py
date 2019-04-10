from django.db import models

# Create your models here.


class SignUp(models.Model):
    email = models.EmailField()
    full_name = models.CharField(max_length=120, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'SignUp'
        verbose_name_plural = 'SingUps'

    def __str__(self):
        return self.email


class Newsletter(models.Model):
    EMAIL_STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    subject = models.CharField(max_length=250)
    body = models.TextField()
    email = models.ManyToManyField(SignUp)
    status = models.CharField(max_length=10, choices=EMAIL_STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
