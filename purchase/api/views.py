from rest_framework import generics, mixins
from purchase.models import PurchaseOrder
from .serializers import PurchaseSerializer
from django.db.models import Q
from .permissions import IsOwnerOrReadOnly


class PurchaseAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'slug'     # (?P<pk>\d+)
    serializer_class = PurchaseSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        qs = PurchaseOrder.objects.all()
        query = self.request.GET.get('q')

        if query is not None:
            qs = qs.filter(Q(title__icontains=query) | Q(content__contains=query)).distinct()

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def supplier(self, request, *args, **kwargs):
        """Give this view the ability to create. Or could just use a mixin"""
        return self.create(request, *args, **kwargs)


class PurchaseRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'     # (?P<pk>\d+)
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        return PurchaseOrder.objects.all()
