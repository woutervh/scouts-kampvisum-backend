from django.db import models

from apps.visums.managers import CampTypeManager

from scouts_auth.inuits.models import AuditedBaseModel
from scouts_auth.inuits.models.fields import RequiredCharField
from scouts_auth.inuits.models.interfaces import Translatable, Explainable

class CampType(Translatable, Explainable, AuditedBaseModel):
    
    objects = CampTypeManager()
    
    camp_type = RequiredCharField()
    )

    class Meta:
        ordering = ["index"]
        unique_together = ("name", "category_set")

    def natural_key(self):
        logger.debug("NATURAL KEY CALLED")
        return (self.name, self.category_set)

    def __str__(self):
        return "OBJECT Category: name({}), category_set({}), index({}), description({})".format(
            self.name, self.category_set, self.index, self.description
        )