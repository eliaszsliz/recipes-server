import graphql_jwt
from .mutations import Register, ObtainJSONWebToken, UserType
import graphene


class Mutation(graphene.ObjectType):
    user_login = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    user_register = Register.Field()


class Query(object):
    user_info = graphene.Field(UserType)

    def resolve_user_info(self, info, **kwargs):
        user = info.context.user
        return user
