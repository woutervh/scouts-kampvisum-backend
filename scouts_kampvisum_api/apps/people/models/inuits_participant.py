from django.db import models

from apps.people.models import InuitsMember, InuitsNonMember

from scouts_auth.inuits.models import AuditedBaseModel
from scouts_auth.inuits.models.fields import OptionalForeignKey


class InuitsParticipant(AuditedBaseModel):

    member = OptionalForeignKey(InuitsMember, on_delete=models.CASCADE)
    non_member = OptionalForeignKey(InuitsNonMember, on_delete=models.CASCADE)

    def has_member(self) -> bool:
        return self.member and self.member.has_group_admin_id()

    def has_non_member(self) -> bool:
        return self.non_member and self.non_member.exists()

    def __str__(self) -> str:
        return "member ({}), non_member ({})".format(self.member, self.non_member)
