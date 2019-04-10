from rest_framework import generics, mixins
from .serializers import RepairSerializer, RepairOrderSerializer
from repairs.models import RepairFile, RepairOrder
from django.db.models import Q
from .permissions import IsOwnerOrReadOnly


class RepairAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'slug'     # (?P<pk>\d+)
    serializer_class = RepairSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        qs = RepairFile.objects.all()
        query = self.request.GET.get('q')

        if query is not None:
            qs = qs.filter(Q(title__icontains=query) | Q(invoice_number__iexact=query)).distinct()

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """Give this view the ability to create. Or could just use a mixin"""
        return self.create(request, *args, **kwargs)


class RepairRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'     # (?P<pk>\d+)
    queryset = RepairFile.objects.all()
    serializer_class = RepairSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        return RepairFile.objects.all()


class RepairOrderAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'slug'     # (?P<pk>\d+)
    serializer_class = RepairOrderSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        qs = RepairOrder.objects.all()
        query = self.request.GET.get('q')

        if query is not None:
            qs = qs.filter(Q(title__icontains=query) | Q(po_number__iexact=query)).distinct()

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """Give this view the ability to create. Or could just use a mixin"""
        return self.create(request, *args, **kwargs)


class RepairOrderRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'     # (?P<pk>\d+)
    queryset = RepairOrder.objects.all()
    serializer_class = RepairOrderSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        return RepairOrder.objects.all()