from django.db import models

from apps.camps.models import Camp, CampType

from apps.visums.managers import CampVisumManager

from scouts_auth.inuits.models import AuditedBaseModel


class CampVisum(AuditedBaseModel):

    objects = CampVisumManager()

    camp = models.ForeignKey(Camp, on_delete=models.CASCADE)
    camp_types = models.ManyToManyField(CampType)

    # class Meta:
    #     ordering = ["camp__sections__name__age_group"]

    def __str__(self):
        return "{}".format(self.id)

    def to_simple_str(self):
        return "{} ({})".format(self.camp.name, self.id)
