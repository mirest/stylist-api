import graphene
import graphql_social_auth
from graphene_django import DjangoObjectType

from apps.permissions.admin import admin_required

from .models import User
from .token import Generate_User


class UserModel(DjangoObjectType):
    class Meta:
        model = User
        exclude_fields = ['password', 'last_login']


class Query(graphene.ObjectType):
    users = graphene.List(UserModel)
    user = graphene.List(UserModel, id=graphene.Int())

    class Arguments:
        name = graphene.Int()

    @admin_required
    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user(self, info, id, **kwargs):
        return User.objects.filter(id=id)


class UserInput(graphene.InputObjectType):
    """
    Class defined to accept input data
    from the interactive graphql console.
    """
    user = graphene.String(required=False)


class LoginUser(graphql_social_auth.SocialAuthMutation):

    user = graphene.Field(UserModel)
    token = graphene.String()
    message = graphene.String(
        required=False, default_value='You have successfully logged in ')

    class Arguments:
        phone_number = graphene.String()
        provider = graphene.String(
            required=False, default_value='google-oauth2')
        access_token = graphene.String(required=True)
        user_type = graphene.String(required=True)

    @classmethod
    def resolve(cls, root, info, social, **kwargs):
        return cls(
            user=social.user, token=Generate_User().generate_token(social.user)
        )


schema = graphene.Schema(query=Query)
