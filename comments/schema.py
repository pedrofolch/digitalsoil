import graphene
from graphene_django.types import DjangoObjectType
from . import models


class CommentType(DjangoObjectType):
    class Meta:
        model = models.Comment


class Query(graphene.AbstractType):
    comments = graphene.List(CommentType)

    def resolve_comments(self, args, context, info):
        return models.Comment.objects.all()
