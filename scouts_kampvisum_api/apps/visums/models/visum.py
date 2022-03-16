from django.db import models

from apps.camps.models import Camp, CampType

from apps.visums.managers import CampVisumManager

from scouts_auth.groupadmin.models import ScoutsGroup

from scouts_auth.inuits.models import AuditedBaseModel


class CampVisum(AuditedBaseModel):

    objects = CampVisumManager()

    group = models.ForeignKey(
        ScoutsGroup, on_delete=models.CASCADE, related_name="visums"
    )
    camp = models.OneToOneField(Camp, on_delete=models.CASCADE, related_name="visum")
    camp_types = models.ManyToManyField(CampType)

    camp_registration_mail_sent_before_deadline = models.BooleanField(default=False)
    # camp_registration_mail_sent_

    # class Meta:
    #     ordering = ["camp__sections__name__age_group"]

    def __str__(self):
        return "{}".format(self.id)

    def to_simple_str(self):
        return "{} ({})".format(self.camp.name, self.id)
