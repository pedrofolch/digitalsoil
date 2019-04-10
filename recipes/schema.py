import graphene
from graphene_django.types import DjangoObjectType
from . import models


class RecipeType(DjangoObjectType):
    class Meta:
        model = models.Recipe


class Query(graphene.AbstractType):
    recipe = graphene.List(RecipeType)

    def resolve_recipe(self, args, context, info):
        return models.Recipe.objects.all()
