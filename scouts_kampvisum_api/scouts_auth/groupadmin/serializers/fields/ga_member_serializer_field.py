import logging

from rest_framework import serializers

from scouts_auth.groupadmin.services import GroupAdmin


logger = logging.getLogger(__name__)


class AbstractScoutsMemberSerializerField(serializers.Field):
    serialize = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data: any) -> dict:
        group_admin_id = data

        if isinstance(data, dict):
            group_admin_id = data.get("group_admin_id")

        return GroupAdmin().get_member_info(active_user=self.context["request"].user, group_admin_id=group_admin_id)

    def to_representation(self, group_admin_id: str) -> dict:
        return GroupAdmin().get_member_info_serialized(
            active_user=self.context["request"].user, group_admin_id=group_admin_id
        )
