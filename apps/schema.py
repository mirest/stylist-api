import graphene


import apps.users.schema
from apps.users.schema import CreateUser


class Query(apps.users.schema.Query):
    pass

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()     

schema = graphene.Schema(query=Query,mutation=Mutation)
