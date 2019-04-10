import graphene
from graphene_django.types import DjangoObjectType
from . import models


class VideoType(DjangoObjectType):
    class Meta:
        model = models.Video


class Query(graphene.AbstractType):
    videos = graphene.List(VideoType)

    def resolve_videos(self, args, context, info):
        return models.Video.objects.all()
