from apps.people.managers import InuitsNonMemberManager

from scouts_auth.groupadmin.scouts import GroupAdminIdField
from scouts_auth.inuits.models import InuitsPerson
from scouts_auth.inuits.models.fields import OptionalCharField


class InuitsNonMember(InuitsPerson):
    objects = InuitsNonMemberManager()

    group_group_admin_id = GroupAdminIdField()
    comment = OptionalCharField(max_length=300)

    class Meta:
        ordering = ["first_name", "last_name", "birth_date", "group_group_admin_id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def exists(self) -> bool:
        return InuitsNonMember.objects.exists(self.id)

    def equals(self, updated_non_member):
        if updated_non_member is None:
            return False

        if not type(updated_non_member).__class__.__name__ == self.__class__.__name__:
            return False

        return (
            self.equals_person(updated_non_member)
            and self.group_group_admin_id == updated_non_member.group_group_admin_id
            and self.comment == updated_non_member.comment
        )

    def __str__(self):
        return "id ({}), group_group_admin_id ({}), {}, comment ({})".format(
            self.id, self.group_group_admin_id, self.person_to_str(), self.comment
        )
