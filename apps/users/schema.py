import graphene
from graphene_django import DjangoObjectType

from .models import User
from .google import Generate_User


class UserModel(DjangoObjectType):
    class Meta:
        model = User
        exclude_fields=['password','last_login']


class Query(graphene.ObjectType):
    users = graphene.List(UserModel)

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

class UserInput(graphene.InputObjectType):
    """
    Class defined to accept input data 
    from the interactive graphql console.
    """
    user = graphene.String(required=False)

class CreateUser(graphene.Mutation):
  
    class Input:
        google_token = graphene.String(required=True)
        phone_number = graphene.String()
        user_type = graphene.String(required=True)

    user = graphene.Field(UserModel)
    token = graphene.String()
    message= graphene.String()

    def mutate(self,*args,**kwargs):
        google=Generate_User(**kwargs)
        user,token,message=google.generate_user()   
        return CreateUser(user=user,token=token,message=message)
    

schema = graphene.Schema(query=Query)

