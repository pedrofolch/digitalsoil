from rest_framework import generics, mixins
from videos.models import Video
from .serializers import VideoSerializer
from django.db.models import Q
from .permissions import IsOwnerOrReadOnly


class VideoAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'     # (?P<pk>\d+)
    serializer_class = VideoSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        qs = Video.objects.all()
        query = self.request.GET.get('q')

        if query is not None:
            qs = qs.filter(Q(title__icontains=query) | Q(content__contains=query)).distinct()

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """Give this view the ability to create. Or could just use a mixin"""
        return self.create(request, *args, **kwargs)


class VideoRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'     # (?P<pk>\d+)
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        return Video.objects.all()
