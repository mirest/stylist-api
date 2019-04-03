import graphene


import apps.users.schema


class Query(apps.users.schema.Query):
    pass


schema = graphene.Schema(query=Query)
