import graphene
from graphene_django.types import DjangoObjectType
from . import models


class PageViewType(DjangoObjectType):
    class Meta:
        model = models.PageView


class Query(graphene.AbstractType):
    analytics = graphene.List(PageViewType)

    def resolve_analytics(self):
        return models.PageView.objects.all()
