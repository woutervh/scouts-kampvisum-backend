from apps.people.managers import InuitsMemberManager

from scouts_auth.groupadmin.scouts import GroupAdminIdField
from scouts_auth.inuits.models import AuditedBaseModel
from scouts_auth.inuits.models.fields import OptionalCharField, DatetypeAwareDateField


class InuitsMember(AuditedBaseModel):
    objects = InuitsMemberManager()

    group_admin_id = GroupAdminIdField()
    first_name = OptionalCharField(max_length=64)
    last_name = OptionalCharField(max_length=128)
    birth_date = DatetypeAwareDateField(blank=True, null=True)

    class Meta:
        ordering = ["first_name", "last_name", "birth_date", "group_admin_id"]

    def equals(self, instance) -> bool:
        if not instance:
            return False

        if not type(instance).__class__.__name__ == "InuitsMember":
            return False

        if (
            self.group_admin_id == instance.group_admin_id
            and self.first_name == instance.first_name
            and self.last_name == instance.last_name
            and self.birth_date == instance.birth_date
        ):
            return True

        return False
