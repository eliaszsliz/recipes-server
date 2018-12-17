import graphene

import recipes.schema
import tokenauth.schema


class Query(recipes.schema.Query, tokenauth.schema.Query, graphene.ObjectType):
    pass


class Mutation(recipes.schema.Mutation, tokenauth.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)
