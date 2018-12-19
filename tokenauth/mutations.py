import graphene
import graphql_jwt
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType
from graphql import GraphQLError



class ErrorType(graphene.ObjectType):
    field = graphene.String()
    message = graphene.String()


class UserType(DjangoObjectType):
    only_fields = ('username', 'id', 'email')
    favoured_ids = graphene.List(graphene.Int)

    class Meta:
        model = User

    def resolve_favoured_ids(self, info):
        return [recipe.pk for recipe in self.favoured.all()]


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info):
        return cls(user=info.context.user)


class Register(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        password_repeat = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(ErrorType)

    def mutate(self, info, email, password, username, password_repeat):
        # todo error handling
        if password == password_repeat:
            try:
                user = User.objects.create(
                    email=email,
                    username=username
                    )
                user.set_password(password)
                user.save()

                return Register(success=bool(user.id))

            except Exception:
                errors = [
                    ErrorType(field='email', message='Email already registered'),
                    ErrorType(field='username', message='Username is '),
                ]
                raise GraphQLError('Email / Username already registered')
                #return Register(success=False, errors=errors)
        # todo check for username too
        errors = [
            ErrorType(field='password', message='Passwords don\'t match'),
        ]
        raise GraphQLError('Passwords don\'t match')
        # return Register(success=False, errors=errors)
