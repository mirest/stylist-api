import graphene
from graphene_django import DjangoObjectType
from .models import Services, HairStyle


class ServiceModel(DjangoObjectType):
    class Meta:
        model = Services


class HairStyleModel(DjangoObjectType):
    class Meta:
        model = HairStyle


class Query(graphene.ObjectType):

    services = graphene.List(ServiceModel, id=graphene.Int())
    hairstyle = graphene.List(HairStyleModel, id=graphene.Int())

    def resolve_services(self, info, id=None, **kwargs):
        if id:
            service_obj = Services.objects.get(pk=id)
            return [service_obj]

        return Services.objects.all()

    def resolve_hairstyle(self, info, id=None, **kwargs):
        if id:
            hair_obj = HairStyle.objects.get(pk=id)
            return [hair_obj]

        return HairStyle.objects.all()
