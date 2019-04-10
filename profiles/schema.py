import graphene
from graphene_django.types import DjangoObjectType
from . import models


class ProfileType(DjangoObjectType):
    class Meta:
        model = models.Profile


class Query(graphene.AbstractType):
    profiles = graphene.List(ProfileType)

    def resolve_profiles(self, args, context, info):
        return models.Profile.objects.all()
