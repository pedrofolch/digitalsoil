import graphene
from graphene_django.types import DjangoObjectType
from . import models


class PostType(DjangoObjectType):
    class Meta:
        model = models.Post


class Query(graphene.AbstractType):
    posts = graphene.List(PostType)

    def resolve_posts(self, args, context, info):
        return models.Post.objects.all()
