from django.db import models
from apps.users.base_model import BaseModel
from apps.users.models import User
from django.db.models.signals import post_save


class BaseProfile(BaseModel):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    sex = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(max_length=100, null=True, blank=True)
    picture = models.URLField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        abstract = True


class ClientProfile(BaseProfile):
    user = models.ForeignKey('users.user',
                             on_delete=models.CASCADE,
                             related_name='client',
                             blank=True)


class StylistProfile(BaseProfile):
    user = models.ForeignKey('users.user',
                             on_delete=models.CASCADE,
                             related_name='stylist',
                             blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)


def user_post_save_receiver(instance, created, *args, **kwargs):
    if instance.user_type == 'stylist':
        model = StylistProfile
    else:
        model = ClientProfile
    if created:
        model.objects.get_or_create(user=instance)


post_save.connect(user_post_save_receiver, sender=User)
