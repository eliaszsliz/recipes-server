import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from recipes.mutations import SetFavourite
from .models import Tag, Recipe





class TagType(DjangoObjectType):
    id = graphene.Int(source='id')
    thumbnail_url = graphene.String(source='thumbnail_url')
    background_url = graphene.String(source='background_url')

    class Meta:
        model = Tag


class RecipeType(DjangoObjectType):
    id = graphene.Int(source='id')
    thumbnail_url = graphene.String(source='thumbnail_url')
    background_url = graphene.String(source='background_url')

    class Meta:
        model = Recipe


class Query(object):
    recipe = graphene.Field(RecipeType,
                            id=graphene.Int(),
                            slug=graphene.String())
    tag = graphene.Field(TagType,
                              id=graphene.Int(),
                              slug=graphene.String())
    all_recipes = graphene.List(RecipeType)
    all_tags = graphene.List(TagType)
    recipes_filter = graphene.List(RecipeType,
                                   query=graphene.String(),
                                   ids=graphene.List(graphene.Int))


    def resolve_all_tags(self, info, **kwargs):
        return Tag.objects.all()

    def resolve_all_recipes(self, info, **kwargs):
        return Recipe.objects.prefetch_related('tags').all()

    def resolve_recipes_filter(self, info, **kwargs):
        query = kwargs.get('query')
        ids = kwargs.get('ids')

        if query is not None:
            return Recipe.objects.filter(slug__icontains=query)

        if ids is not None:
            return Recipe.objects.filter(id__in=ids)

        return Recipe.objects.none()


    def resolve_recipe(self, info, **kwargs):
        id = kwargs.get('id')
        slug = kwargs.get('slug')

        if id is not None:
            return Recipe.objects.get(pk=id)

        if slug is not None:
            return Recipe.objects.get(slug=slug)

        return None

    def resolve_tag(self, info, **kwargs):
        id = kwargs.get('id')
        slug = kwargs.get('slug')

        if id is not None:
            return Tag.objects.get(pk=id)

        if slug is not None:
            return Tag.objects.get(slug=slug)
        return None


class Mutation(graphene.ObjectType):
    set_favourite = SetFavourite.Field()