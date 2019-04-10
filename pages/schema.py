import graphene
from graphene_django.types import DjangoObjectType
from . import models


class PageType(DjangoObjectType):
    class Meta:
        model = models.Page


class Query(graphene.AbstractType):
    pages = graphene.List(PageType)

    def resolve_pages(self, args, context, info):
        return models.Page.objects.all()
