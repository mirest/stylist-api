import graphene
from graphene_django import DjangoObjectType

from .models import ClientProfile, StylistProfile


class ClientProfileModel(DjangoObjectType):
    class Meta:
        model = ClientProfile


class StylistProfileModel(DjangoObjectType):
    class Meta:
        model = StylistProfile


class Query(graphene.ObjectType):
    client_profiles = graphene.List(ClientProfileModel, id=graphene.Int())
    stylist_profiles = graphene.List(StylistProfileModel, id=graphene.Int())

    def resolve_stylist_profiles(self, info, id=None, **kwargs):
        if id:
            return [StylistProfile.objects.get(pk=id)]
        return StylistProfile.objects.all()

    def resolve_client_profiles(self, info, id=None, **kwargs):
        if id:
            return [ClientProfile.objects.get(pk=id)]
        return ClientProfile.objects.all()


schema = graphene.Schema(query=Query)
