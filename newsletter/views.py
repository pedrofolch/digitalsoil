from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template

from .models import SignUp, Newsletter
from .forms import SignUpForm, NewsletterCreationForm, ContactForm


def home(request):
    title = 'Join Us!'
    form = SignUpForm(request.POST or None)

    context = {
        "title": title,
        "form": form,
    }

    if form.is_valid():
        instance = form.save(commit=False)
        if not instance.full_name:
            instance.full_name = "Visitor"
        instance.save()

        context = {
            "title": "Thank you!"
        }

        if request.user.is_authenticated() and request.user.is_staff:
            print(SignUp.objects.all())
            for instance in SignUp.objects.all():
                print(instance.full_name)
            queryset = SignUp.objects.all().order_by("-timestamp")
            print(SignUp.objects.all().order_by("-timestamp").filter(full_name__icontains="Pedro").count())

            context = {
                "queryset": queryset,
            }

        if SignUp.objects.filter(email=instance.email).exists():
            messages.warning(request,
                             "Your Email Already exists in our database",
                             "alert alert-warning alert-dismissible")
        else:
            instance.save()
            messages.success(request,
                             "Your email has been submitted",
                             "alert alert-success alert-dismissible")
            # form_email = form.cleaned_data.get('email')
            # form_message = form.cleaned_data.get('message')
            # form_full_name = form.cleaned_data.get('full_name')
            subject = "Digital Soil Thanks You for joining our Newsletter"
            from_email = settings.EMAIL_HOST_USER
            to_email = [instance.email, settings.EMAIL_HOST_USER]
            # contact_message = "%s: %s via %s" % (
            #     form_full_name,
            #     form_message,
            #     form_email
            # )
            # to send text and html emails
            with open(settings.BASE_DIR + '/templates/newsletters/sign_up_email.txt') as f:
                signup_message = f.read()
            message = EmailMultiAlternatives(subject=subject, body=signup_message, from_email=from_email, to=to_email, )
            html_template = get_template("newsletters/sign_up_email.html").render()
            message.attach_alternative(html_template, "text/html")
            message.send()
            signup_message = """Welcome to Digital Soil Newsletter. \
             If you would like to unsubscribe visit http://digitalearth.herokuapp/newsletter/unsubscribe"""
            send_mail(subject=subject,
                      message=signup_message,
                      from_email=from_email,
                      recipient_list=to_email,
                      fail_silently=False,
                      )
            messages.success(request, 'Thanks for joining.')

    context = {
        'form': form,
    }
    template = "newsletters/sign_up.html"
    return render(request, template, context)


def newsletter_unsubscribe(request):
    form = SignUpForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        if SignUp.objects.filter(email=instance.email).exists():
            SignUp.objects.filter(email=instance.email).delete()
            messages.success(request,
                             "Your email has been removed",
                             'alert alert-success alert-dismissible')
            subject = 'You have unsubscribed '
            from_email = settings.EMAIL_HOST_USER
            to_email = [instance.email, settings.EMAIL_HOST_USER]
            with open(settings.BASE_DIR + '/templates/newsletters/unsubscribe_email.txt') as f:
                signup_message = f.read()
            message = EmailMultiAlternatives(subject=subject, body=signup_message, from_email=from_email, to=to_email, )
            html_template = get_template("newsletters/unsubscribe_email.html").render()
            message.attach_alternative(html_template, "text/html")
            message.send()
        else:
            messages.warning(request,
                             'Your emial. in not in the database',
                             'alert alert-warning alert-dismissible')

    context = {
        'form': form,
    }
    template = 'newsletters/sign_up.html'
    return render(request, template, context)


def control_newsletter(request):
    form = NewsletterCreationForm(request.POST or None)

    if form.is_valid():
        instance = form.save()
        newsletter = Newsletter.objects.get(id=instance.id)
        if newsletter.status == "Publish":
            subject = newsletter.subject
            body = newsletter.body
            from_email = settings.EMAIL_HOST_USER
            for email in newsletter.email.all():
                send_mail(subject=subject, from_email=from_email,
                          recipient_list=[email], message=body, fail_silently=True)

    context = {
        'form': form,
    }

    template = 'newsletters/control_newsletter.html'
    return render(request, template, context)


def contact(request):
    title = "Contact Us"
    title_align_center = True
    form = ContactForm(request.POST or None)
    if form.is_valid():
        # for key, value in form.cleaned_data.iteritems():
        #     print key, value
        #     #print form.cleaned_data.get(key)
        form_email = form.cleaned_data.get("email")
        form_message = form.cleaned_data.get("message")
        form_full_name = form.cleaned_data.get("full_name")
        # print(email, message, full_name)
        subject = 'Site contact form'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email]
        contact_message = "%s: %s via %s" % (
            form_full_name,
            form_message,
            form_email)
        html_message = "<h1>Hello</h1>"
        send_mail(subject,
                  contact_message,
                  from_email,
                  [to_email],
                  html_message=html_message,
                  fail_silently=False)
    context = {
        "form": form,
        "title": title,
        "title_align_center": title_align_center,
    }

    return render(request, "newsletters/forms.html", context)
