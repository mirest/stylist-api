import graphene
import apps.users.schema
from apps.users.schema import LoginUser
import apps.services.schema


class Query(apps.users.schema.Query, apps.services.schema.Query):
    pass


class Mutation(graphene.ObjectType):
    login = LoginUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
