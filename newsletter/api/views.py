from rest_framework import generics

from newsletter.models import SignUp
from .serializers import SignUpSerializer


class SignUpCreateAPIView(generics.CreateAPIView):
    queryset = SignUp.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = []
    authentication_classes = []
