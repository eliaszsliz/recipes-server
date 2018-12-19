import graphene
from graphql import GraphQLError

from tokenauth.mutations import ErrorType
from .models import Recipe


class SetFavourite(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        new_value = graphene.Boolean(required=False)

    success = graphene.Boolean()
    errors = graphene.List(ErrorType)

    def mutate(self, info, id, new_value=None):
        user = info.context.user
        print(user)

        try:
            Recipe.objects.get(id=id).set_favourite(user, new_value)
            return SetFavourite(success=bool(user.id))
        except Recipe.DoesNotExtists:
            raise GraphQLError('Theres no Recipe with this id')
