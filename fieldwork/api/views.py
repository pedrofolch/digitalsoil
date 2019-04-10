from rest_framework import generics, mixins
from fieldwork.models import FieldData
from .serializers import FieldWorkSerializer
from django.db.models import Q
from .permissions import IsOwnerOrReadOnly


class FieldWorkAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'     # (?P<pk>\d+)
    serializer_class = FieldWorkSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        qs = FieldData.objects.all()
        query = self.request.GET.get('q')

        if query is not None:
            qs = qs.filter(Q(pile_name__icontains=query) |
                           Q(new_pile_name=query) |
                           Q(content__contains=query)).distinct()

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def fielddata(self, request, *args, **kwargs):
        """Give this view the ability to create. Or could just use a mixin"""
        return self.create(request, *args, **kwargs)


class FieldWorkRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'     # (?P<pk>\d+)
    queryset = FieldData.objects.all()
    serializer_class = FieldWorkSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        return FieldData.objects.all()
