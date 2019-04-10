from rest_framework import generics, mixins
from labsoil.models import Lab
from .serializers import LabPostSerializer
from django.db.models import Q
from .permissions import IsOwnerOrReadOnly


class LabPostAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'     # (?P<pk>\d+)
    serializer_class = LabPostSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        qs = Lab.objects.all()
        query = self.request.GET.get('q')

        if query is not None:
            qs = qs.filter(Q(title__icontains=query) |
                           Q(sample_id__contains=query) |
                           Q(content__contains=query)).distinct()

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """Give this view the ability to create. Or could just use a mixin"""
        return self.create(request, *args, **kwargs)


class LabPostRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'     # (?P<pk>\d+)
    queryset = Lab.objects.all()
    serializer_class = LabPostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        return Lab.objects.all()
