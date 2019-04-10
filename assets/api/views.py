from rest_framework import generics, mixins
from .serializers import TypeOfAssetSerializer, MarineVesselSerializer, \
    AutomobileSerializer, EquipmentAssetSerializer, \
    AssetSerializer, PartsSerializer, CarManufacturerSerializer, \
    MarineVesselManufacturerSerializer, EquipmentManufacturerSerializer, CarModelTypeSerializer, \
    MarineModelTypeSerializer, EquipmentModelTypeSerializer, ThroughHullSerializer
from assets.models import TypeOfAsset, MarineVessel, Automobile, Equipment, \
    Parts, CarManufacturer, MarineVesselManufacturer, EquipmentManufacturer, \
    CarModelType, MarineModelType, EquipmentModelType, ThroughHull, Asset
from django.db.models import Q
from .permissions import IsOwnerOrReadOnly


class AssetAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'slug'     # (?P<pk>\d+)
    serializer_class = TypeOfAssetSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        qs = TypeOfAsset.objects.all()
        query = self.request.GET.get('q')

        if query is not None:
            qs = qs.filter(Q(title__icontains=query) | Q(content__contains=query)).distinct()

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """Give this view the ability to create. Or could just use a mixin"""
        return self.create(request, *args, **kwargs)


class AssetRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'     # (?P<pk>\d+)
    queryset = TypeOfAsset.objects.all()
    serializer_class = TypeOfAssetSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        return TypeOfAsset.objects.all()


class MarineAssetAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'slug'     # (?P<pk>\d+)
    serializer_class = MarineVesselSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        qs = MarineVessel.objects.all()
        query = self.request.GET.get('q')

        if query is not None:
            qs = qs.filter(Q(title__icontains=query) | Q(content__contains=query)).distinct()

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """Give this view the ability to create. Or could just use a mixin"""
        return self.create(request, *args, **kwargs)


class MarineAssetRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'     # (?P<pk>\d+)
    queryset = MarineVessel.objects.all()
    serializer_class = MarineVesselSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        return MarineVessel.objects.all()


class LandAssetAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'slug'     # (?P<pk>\d+)
    serializer_class = AutomobileSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        qs = Automobile.objects.all()
        query = self.request.GET.get('q')

        if query is not None:
            qs = qs.filter(Q(title__icontains=query) | Q(content__contains=query)).distinct()

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """Give this view the ability to create. Or could just use a mixin"""
        return self.create(request, *args, **kwargs)


class LandAssetRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'     # (?P<pk>\d+)
    queryset = Automobile.objects.all()
    serializer_class = AutomobileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        return Automobile.objects.all()


class EquipmentAssetAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'slug'     # (?P<pk>\d+)
    serializer_class = EquipmentAssetSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        qs = Equipment.objects.all()
        query = self.request.GET.get('q')

        if query is not None:
            qs = qs.filter(Q(title__icontains=query) | Q(content__contains=query)).distinct()

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """Give this view the ability to create. Or could just use a mixin"""
        return self.create(request, *args, **kwargs)


class EquipmentAssetRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'     # (?P<pk>\d+)
    queryset = Equipment.objects.all()
    serializer_class = EquipmentAssetSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        return Equipment.objects.all()


class AssetAssetAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'     # (?P<pk>\d+)
    serializer_class = AssetSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        qs = Asset.objects.all()
        query = self.request.GET.get('q')

        if query is not None:
            qs = qs.filter(Q(title__icontains=query) | Q(content__contains=query)).distinct()

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """Give this view the ability to create. Or could just use a mixin"""
        return self.create(request, *args, **kwargs)


class AssetAssetRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'     # (?P<pk>\d+)
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        return Asset.objects.all()


class PartsAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'     # (?P<pk>\d+)
    serializer_class = PartsSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        qs = Parts.objects.all()
        query = self.request.GET.get('q')

        if query is not None:
            qs = qs.filter(Q(title__icontains=query) | Q(content__contains=query)).distinct()

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """Give this view the ability to create. Or could just use a mixin"""
        return self.create(request, *args, **kwargs)


class PartsRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'     # (?P<pk>\d+)
    queryset = Parts.objects.all()
    serializer_class = PartsSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        return Parts.objects.all()


class CarManufacturerAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'     # (?P<pk>\d+)
    serializer_class = CarManufacturerSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        qs = CarManufacturer.objects.all()
        query = self.request.GET.get('q')

        if query is not None:
            qs = qs.filter(Q(title__icontains=query)).distinct()

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """Give this view the ability to create. Or could just use a mixin"""
        return self.create(request, *args, **kwargs)


class CarManufacturerRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'     # (?P<pk>\d+)
    queryset = CarManufacturer.objects.all()
    serializer_class = CarManufacturerSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        return CarManufacturer.objects.all()


class MarineVesselManufacturerSerializerAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'     # (?P<pk>\d+)
    serializer_class = MarineVesselManufacturerSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        qs = MarineVesselManufacturer.objects.all()
        query = self.request.GET.get('q')

        if query is not None:
            qs = qs.filter(Q(title__icontains=query)).distinct()

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """Give this view the ability to create. Or could just use a mixin"""
        return self.create(request, *args, **kwargs)


class MarineVesselManufacturerRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'     # (?P<pk>\d+)
    queryset = MarineVesselManufacturer.objects.all()
    serializer_class = MarineVesselManufacturerSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        return MarineVesselManufacturer.objects.all()


class EquipmentManufacturerAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'     # (?P<pk>\d+)
    serializer_class = EquipmentManufacturerSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        qs = EquipmentManufacturer.objects.all()
        query = self.request.GET.get('q')

        if query is not None:
            qs = qs.filter(Q(title__icontains=query)).distinct()

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """Give this view the ability to create. Or could just use a mixin"""
        return self.create(request, *args, **kwargs)


class EquipmentManufacturerRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'     # (?P<pk>\d+)
    queryset = EquipmentManufacturer.objects.all()
    serializer_class = EquipmentManufacturerSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        return EquipmentManufacturer.objects.all()


class CarModelTypeAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'     # (?P<pk>\d+)
    serializer_class = CarModelTypeSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        qs = CarModelType.objects.all()
        query = self.request.GET.get('q')

        if query is not None:
            qs = qs.filter(Q(title__icontains=query)).distinct()

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """Give this view the ability to create. Or could just use a mixin"""
        return self.create(request, *args, **kwargs)


class CarModelTypeRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'     # (?P<pk>\d+)
    queryset = CarModelType.objects.all()
    serializer_class = CarModelTypeSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        return CarModelType.objects.all()


class MarineModelTypeAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'     # (?P<pk>\d+)
    serializer_class = MarineModelTypeSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        qs = MarineModelType.objects.all()
        query = self.request.GET.get('q')

        if query is not None:
            qs = qs.filter(Q(title__icontains=query)).distinct()

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """Give this view the ability to create. Or could just use a mixin"""
        return self.create(request, *args, **kwargs)


class MarineModelTypeRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'     # (?P<pk>\d+)
    queryset = MarineModelType.objects.all()
    serializer_class = MarineModelTypeSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        return MarineModelType.objects.all()


class EquipmentModelTypeAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'     # (?P<pk>\d+)
    serializer_class = EquipmentModelTypeSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        qs = EquipmentModelType.objects.all()
        query = self.request.GET.get('q')

        if query is not None:
            qs = qs.filter(Q(title__icontains=query) | Q(content__contains=query)).distinct()

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """Give this view the ability to create. Or could just use a mixin"""
        return self.create(request, *args, **kwargs)


class EquipmentModelTypeRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'     # (?P<pk>\d+)
    queryset = EquipmentModelType.objects.all()
    serializer_class = EquipmentModelTypeSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        return EquipmentModelType.objects.all()


class ThroughHullAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'     # (?P<pk>\d+)
    serializer_class = ThroughHullSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        qs = ThroughHull.objects.all()
        query = self.request.GET.get('q')

        if query is not None:
            qs = qs.filter(Q(title__icontains=query) | Q(content__contains=query)).distinct()

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """Give this view the ability to create. Or could just use a mixin"""
        return self.create(request, *args, **kwargs)


class ThroughHullRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'     # (?P<pk>\d+)
    queryset = ThroughHull.objects.all()
    serializer_class = ThroughHullSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        return ThroughHull.objects.all()
