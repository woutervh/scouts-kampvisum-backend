from django.db import models

from apps.people.models import InuitsMember, InuitsNonMember

from scouts_auth.inuits.models import AuditedBaseModel
from scouts_auth.inuits.models.fields import OptionalForeignKey


class InuitsParticipant(AuditedBaseModel):

    member = OptionalForeignKey(InuitsMember, on_delete=models.CASCADE)
    non_member = OptionalForeignKey(InuitsNonMember, on_delete=models.CASCADE)
