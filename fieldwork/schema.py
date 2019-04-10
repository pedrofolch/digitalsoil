import graphene
from graphene_django.types import DjangoObjectType
from . import models


class FieldDataType(DjangoObjectType):
    class Meta:
        model = models.FieldData


class Query(graphene.AbstractType):
    fieldwork = graphene.List(FieldDataType)

    def resolve_fieldwork(self, args, context, info):
        return models.FieldData.objects.all()
