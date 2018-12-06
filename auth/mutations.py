import graphene
from django.contrib.auth.models import User
from graphql import GraphQLError


class Error(graphene.ObjectType):
    field = graphene.String()
    message = graphene.String()


class Register(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        password_repeat = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(Error)

    def mutate(self, info, email, password, username, password_repeat):
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
                    Error(field='email', message='Email already registered'),
                    Error(field='username', message='Username is '),
                ]
                raise GraphQLError('Email / Username already registered')
                #return Register(success=False, errors=errors)
        # todo check for username too
        errors = [
            Error(field='password', message='Passwords don\'t match'),
        ]
        raise GraphQLError('Passwords don\'t match')
        # return Register(success=False, errors=errors)
