from rest_framework import generics, mixins
from recipes.models import Recipe
from .serializers import RecipeSerializer
from django.db.models import Q
from .permissions import IsOwnerOrReadOnly


class RecipeAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'slug'     # (?P<pk>\d+)
    serializer_class = RecipeSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        qs = Recipe.objects.all()
        query = self.request.GET.get('q')

        if query is not None:
            qs = qs.filter(Q(title__icontains=query) | Q(content__contains=query)).distinct()

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def recipe(self, request, *args, **kwargs):
        """Give this view the ability to create. Or could just use a mixin"""
        return self.create(request, *args, **kwargs)


class RecipeRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'     # (?P<pk>\d+)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        return Recipe.objects.all()
