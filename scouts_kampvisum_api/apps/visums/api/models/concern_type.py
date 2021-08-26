from django.db import models

from apps.base.models import BaseModel
from inuits.models import RequiredCharField


class CampVisumConcernType(BaseModel):

    type = RequiredCharField(max_length=32)
