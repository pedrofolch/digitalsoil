import graphene
from graphene_django.types import DjangoObjectType
from . import models


class LabType(DjangoObjectType):
    class Meta:
        model = models.Lab


class Query(graphene.AbstractType):
    labs = graphene.List(LabType)

    def resolve_labs(self, args, context, info):
        return models.Lab.objects.all()
