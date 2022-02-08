from django.db import models

from apps.camps.models import CampType

from apps.deadlines.models import DefaultDeadline

from scouts_auth.inuits.models import AuditedBaseModel

class DeadlineSet(AuditedBaseModel):
    
    camp_type = models.ForeignKey(CampType, on_delete=models.CASCADE, related_name="deadline_set")
    deadlines = models.ManyToManyField(DefaultDeadline)
