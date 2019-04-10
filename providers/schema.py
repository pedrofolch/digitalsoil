import graphene
from graphene_django.types import DjangoObjectType
from . import models


class SupplierType(DjangoObjectType):
    class Meta:
        model = models.Supplier


class Query(graphene.AbstractType):
    suppliers = graphene.List(SupplierType)

    def resolve_suppliers(self, args, context, info):
        return models.Supplier.objects.all()
