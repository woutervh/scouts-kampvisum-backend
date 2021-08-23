from django.db import models

from apps.base.models import BaseModel
from apps.scouts_groups.api.groups.models import ScoutsGroup

class ScoutsCampVisum(BaseModel):

    group = models.ForeignKey(ScoutsGroup)