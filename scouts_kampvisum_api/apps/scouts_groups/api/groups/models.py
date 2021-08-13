from django.db import models

from scouts_auth.models import ScoutsAuthGroup
from ....base.models import BaseModel


class ScoutsGroupType(BaseModel):
    """
    Specifies the type of scouts group (e.g. AKABE, zeescouts, ...).
    """
    
    type = models.CharField(max_length=64)
    
    class Meta:
        ordering = ['type']
    
    def clean(self):
        pass


class ScoutsGroup(BaseModel):
    """
    A ScoutsGroup.
    
    Data is loaded with a call to the ScoutsGroupService, using the name
    
    ScoutsAuthGroup fields:
    id = models.AutoField(
        primary_key=True, editable=False)
    name = models.CharField(
        max_length=128)
    location = models.CharField(
        max_length=128)
    uuid = models.UUIDField(
        primary_key=False, default=uuid.uuid4(), editable=False, unique=True)
    """
    
    type = models.ForeignKey(ScoutsGroupType, on_delete=models.CASCADE)
    
    def clean(self):
        pass

