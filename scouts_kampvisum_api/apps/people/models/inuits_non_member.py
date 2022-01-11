from scouts_auth.groupadmin.scouts import GroupAdminIdField
from scouts_auth.inuits.models import InuitsPerson
from scouts_auth.inuits.models.fields import OptionalCharField


class InuitsNonMember(InuitsPerson):
    group_admin_id = GroupAdminIdField()
    comment = OptionalCharField(max_length=300)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
