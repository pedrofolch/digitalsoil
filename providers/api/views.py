from rest_framework import generics, mixins
from providers.models import Supplier
from .serializers import SupplierSerializer
from django.db.models import Q
from .permissions import IsOwnerOrReadOnly


class SupplierAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'slug'     # (?P<pk>\d+)
    serializer_class = SupplierSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        qs = Supplier.objects.all()
        query = self.request.GET.get('q')

        if query is not None:
            qs = qs.filter(Q(title__icontains=query) | Q(content__contains=query)).distinct()

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def supplier(self, request, *args, **kwargs):
        """Give this view the ability to create. Or could just use a mixin"""
        return self.create(request, *args, **kwargs)


class SupplierRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'     # (?P<pk>\d+)
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        return Supplier.objects.all()
