import graphene
from graphene_django.types import DjangoObjectType
from graphene import relay, ObjectType, Node
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Tag, Recipe


class TagType(DjangoObjectType):
    class Meta:
        model = Tag


class RecipeType(DjangoObjectType):
    thumbnail_url = graphene.String(source='thumbnail_url')
    background_url = graphene.String(source='background_url')

    class Meta:
        model = Recipe
        # filter_fields = {
        #     'name': ['exact', 'icontains', 'istartswith'],
        #     'tags': ['exact', 'icontains'],
        #     'difficulty': ['exact', 'icontains'],
        # }


class Query(object):
    recipe = graphene.Field(RecipeType,
                              id=graphene.Int(),
                              slug=graphene.String())
    tag = graphene.Field(TagType,
                              id=graphene.Int(),
                              slug=graphene.String())
    all_recipes = graphene.List(RecipeType)
    all_tags = graphene.List(TagType)
    search_recipes = graphene.List(RecipeType, query=graphene.String())

    def resolve_all_tags(self, info, **kwargs):
        return Tag.objects.all()

    def resolve_all_recipes(self, info, **kwargs):
        return Recipe.objects.prefetch_related('tags').all()

    def resolve_search_recipes(self, info, **kwargs):
        query = kwargs.get('query')

        if query is not None:
            return Recipe.objects.filter(slug__icontains=query)

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