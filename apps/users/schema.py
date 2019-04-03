import graphene
from graphene_django import DjangoObjectType

from .models import User


class UserModel(DjangoObjectType):
    class Meta:
        model = User


class Query(graphene.ObjectType):
    users = graphene.List(UserModel)

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

class Mutation(graphene.ObjectType):
    pass

# schema = graphene.Schema(query=Query, mutation=Mutation)
schema = graphene.Schema(query=Query)
