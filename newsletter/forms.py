from django import forms

from newsletter.models import SignUp, Newsletter


class ContactForm(forms.Form):
    full_name = forms.CharField(required=False)
    email = forms.EmailField()
    message = forms.CharField()


class SignUpForm(forms.ModelForm):
    email = forms.EmailField(label="",
                             widget=forms.EmailInput(attrs={
                                 'placeholder': 'Your email',
                                 'class': 'form-control'
                             }))

    class Meta:
        model = SignUp
        fields = [
            'email'
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        # email_base, provider = email.split("@")
        # if not provider == 'gmail.com':
        #     raise forms.ValidationError("Please use a valid Gmail email address")
        print(email)
        qs = SignUp.objects.filter(email__iexact=email)
        if qs.exists():
            print('exists')
            raise forms.ValidationError("This email already exists")
        return email

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        return full_name


class NewsletterCreationForm(forms.ModelForm):

    class Meta:
        model = Newsletter
        fields = [
            'subject',
            'body',
            'email',
            'status'
        ]
