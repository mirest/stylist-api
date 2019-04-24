from django.db import models
from apps.users.base_model import BaseModel
from django.contrib.auth import get_user_model as user_model
from django.contrib.postgres.fields.ranges import IntegerRangeField

User = user_model()


class Services(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    tag = models.TextField()


class HairStyle(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    picture = models.URLField()
    slug = models.SlugField()
    price_range = IntegerRangeField(default=0)
    stylist = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)

    class Meta:
        ordering = ['price_range']
