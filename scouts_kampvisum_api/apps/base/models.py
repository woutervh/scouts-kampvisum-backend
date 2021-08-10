import uuid
from django.db import models
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE

from scouts_auth.models import ScoutsAuthGroup


class BaseModel(SafeDeleteModel):
    
    _safedelete_policy = SOFT_DELETE
    
    id = models.UUIDField(
        primary_key=True, editable = False, default=uuid.uuid4)
    
    class Meta:
        abstract = True


class ScoutsGroup(ScoutsAuthGroup):
    pass

