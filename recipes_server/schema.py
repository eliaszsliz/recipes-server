import graphene

import recipes.schema
import auth.schema


class Query(recipes.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(
    query=Query,
    mutation=auth.schema.Mutation
)
