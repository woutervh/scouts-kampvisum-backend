from apps.participants.managers import InuitsParticipantManager

from scouts_auth.groupadmin.scouts import GroupAdminIdField
from scouts_auth.inuits.models import InuitsPerson
from scouts_auth.inuits.models.fields import OptionalCharField


class InuitsParticipant(InuitsPerson):
    objects = InuitsParticipantManager()

    group_group_admin_id = GroupAdminIdField()
    group_admin_id = GroupAdminIdField()
    comment = OptionalCharField(max_length=300)

    class Meta:
        ordering = ["first_name", "last_name", "birth_date", "group_group_admin_id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
            and self.comment == updated_participant.comment
        )

    def __str__(self):
        return "id ({}), group_group_admin_id ({}), group_admin_id ({}), {}, comment ({})".format(
            self.id,
            self.group_group_admin_id,
            self.group_group_admin_id,
            self.person_to_str(),
            self.comment,
        )
