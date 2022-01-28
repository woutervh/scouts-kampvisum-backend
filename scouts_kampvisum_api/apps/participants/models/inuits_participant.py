from django.db import models

from apps.participants.managers import InuitsParticipantManager

from scouts_auth.groupadmin.scouts import GroupAdminIdField
from scouts_auth.groupadmin.models import AbstractScoutsMember

from scouts_auth.inuits.models import InuitsPerson
from scouts_auth.inuits.models.fields import OptionalCharField


class InuitsParticipant(InuitsPerson):
    objects = InuitsParticipantManager()

    group_group_admin_id = GroupAdminIdField(null=True)
    group_admin_id = GroupAdminIdField(null=True)
    is_member = models.BooleanField(default=False)
    comment = OptionalCharField(max_length=300)

    class Meta:
        ordering = ["first_name", "last_name", "birth_date", "group_group_admin_id"]
        constraints = [
            models.UniqueConstraint(fields=["email"], name="unique_email"),
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def has_group_admin_id(self) -> bool:
        return hasattr(self, "group_admin_id") and self.group_admin_id

    def exists(self) -> bool:
        return InuitsParticipant.objects.exists(self.id)

    def equals(self, updated_participant):
        if updated_participant is None:
            return False

        if not type(updated_participant).__class__.__name__ == self.__class__.__name__:
            return False

        return (
            self.equals_person(updated_participant)
            and self.group_group_admin_id == updated_participant.group_group_admin_id
            and self.group_admin_id == updated_participant.group_group_admin_id
            and self.is_member == updated_participant.is_member
            and self.comment == updated_participant.comment
        )

    def __str__(self):
        return "id ({}), is_member ({}), group_group_admin_id ({}), group_admin_id ({}), {}, comment ({})".format(
            self.id,
            self.is_member,
            self.group_group_admin_id,
            self.group_admin_id,
            self.person_to_str(),
            self.comment,
        )

    @staticmethod
    def from_scouts_member(scouts_member: AbstractScoutsMember):
        participant = InuitsParticipant()

        participant.id = None
        participant.is_member = True
        participant.first_name = scouts_member.first_name
        participant.last_name = scouts_member.last_name
        participant.phone_number = scouts_member.phone_number
        participant.cell_number = scouts_member.cell_number
        participant.email = scouts_member.email
        participant.birth_date = scouts_member.birth_date
        participant.gender = scouts_member.gender
        participant.street = scouts_member.street
        participant.number = scouts_member.number
        participant.letter_box = scouts_member.letter_box
        participant.postal_code = scouts_member.postal_code
        participant.city = scouts_member.city
        participant.group_group_admin_id = ""
        participant.group_admin_id = scouts_member.group_admin_id
        participant.comment = ""

        return participant
