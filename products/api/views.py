from rest_framework import generics, mixins, pagination
from rest_framework.response import Response

from products.models import Product
from .serializers import ProductSerializer
from django.db.models import Q
from .permissions import IsOwnerOrReadOnly


class ProductAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'     # (?P<pk>\d+)
    serializer_class = ProductSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        qs = Product.objects.all()
        query = self.request.GET.get('q')

        if query is not None:
            qs = qs.filter(Q(title__icontains=query) | Q(content__contains=query)).distinct()

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def product(self, request, *args, **kwargs):
        """Give this view the ability to create. Or could just use a mixin"""
        return self.create(request, *args, **kwargs)


class ProductRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'     # (?P<pk>\d+)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        """Could override"""
        return Product.objects.all()


class ProductPageNumberPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'size'
    max_page_size = 20

    def get_paginated_response(self, data):
        author = False
        user = self.request.user
        if user.is_authenticated:
            author = True
        context = {
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'author': author,
            'results': data,
        }
        return Response(context)
