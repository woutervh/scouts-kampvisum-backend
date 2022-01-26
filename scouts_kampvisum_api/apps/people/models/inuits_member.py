from apps.people.managers import InuitsMemberManager

from scouts_auth.groupadmin.scouts import GroupAdminIdField
from scouts_auth.groupadmin.models import AbstractScoutsMember
from scouts_auth.inuits.models import AuditedBaseModel
from scouts_auth.inuits.models.fields import OptionalCharField, DatetypeAwareDateField


class InuitsMember(AuditedBaseModel):
    objects = InuitsMemberManager()

    group_admin_id = GroupAdminIdField()
    first_name = OptionalCharField(max_length=64)
    last_name = OptionalCharField(max_length=128)
    email = OptionalCharField(max_length=128)
    birth_date = DatetypeAwareDateField(blank=True, null=True)

    class Meta:
        ordering = ["first_name", "last_name", "birth_date", "group_admin_id"]

    def has_group_admin_id(self) -> bool:
        return self.group_admin_id

    def equals(self, instance) -> bool:
        if not instance:
            return False

        if not type(instance).__class__.__name__ == "InuitsMember":
            return False

        if (
            self.group_admin_id == instance.group_admin_id
            and self.first_name == instance.first_name
            and self.last_name == instance.last_name
            and self.email == instance.email
            and self.birth_date == instance.birth_date
        ):
            return True

        return False

    @staticmethod
    def from_scouts_member(scouts_member: AbstractScoutsMember):
        member = InuitsMember()

        member.group_admin_id = scouts_member.group_admin_id
        member.first_name = scouts_member.first_name
        member.last_name = scouts_member.last_name
        member.email = scouts_member.email
        member.birth_date = scouts_member.birth_date

        return member

    def __str__(self):
        return "group_admin_id ({}), first_name ({}), last_name ({}), email ({}), birth_date ({})".format(
            self.group_admin_id,
            self.first_name,
            self.last_name,
            self.email,
            self.birth_date,
        )
