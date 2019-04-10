from rest_framework import serializers

from newsletter.models import SignUp


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = SignUp
        fields = ['email']

    def validate_email(self, value):
        email = value
        qs = SignUp.objects.filter(email__iexact=email)
        if qs.exists():
            raise serializers.ValidationError("This email already exists")
        return email
