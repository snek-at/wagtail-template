from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import (
    login_required,
    permission_required,
    staff_member_required,
    superuser_required,
)

from .models import User

# Create your user related graphql schemes here.

# Create your user related graphql schemes here.


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        exclude = ["password"]


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    @superuser_required
    def mutate(self, info, username, password, email):
        user = get_user_model()(username=username, email=email,)

        user.set_password(password)
        user.save()
        # saved to our user objects as a wagtail user

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


class GetUsers(graphene.ObjectType):
    me = graphene.Field(UserType, token=graphene.String(required=False))
    user = graphene.Field(
        UserType,
        token=graphene.String(required=False),
        username=graphene.String(required=True),
    )
    users = graphene.List(UserType, token=graphene.String(required=False))

    @login_required
    def resolve_me(self, info):
        user = info.context.user
        return user

    @login_required
    def resolve_user(self, info, username, **_kwargs):
        user = get_user_model().objects.get(username=f"{username}")
        return user

    @superuser_required
    def resolve_users(self, info):
        # To list all users
        return get_user_model().objects.all()
