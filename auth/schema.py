import graphene
import graphql_jwt
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType

from auth.mutations import Register


class UserType(DjangoObjectType):
    only_fields = ('username', 'id', 'email')

    class Meta:
        model = User


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info):
        return cls(user=info.context.user)


class Mutation(graphene.ObjectType):
    user_login = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    user_register = Register.Field()
