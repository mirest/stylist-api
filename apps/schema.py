import graphene
import apps.users.schema
from apps.users.schema import LoginUser


class Query(apps.users.schema.Query):
    pass


class Mutation(graphene.ObjectType):
    login = LoginUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
