from typing import List

from rest_framework import serializers

from scouts_auth.groupadmin.models import ScoutsUser, ScoutsGroup

from scouts_auth.inuits.utils import ListUtils


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsUserSerializer(serializers.ModelSerializer):

    user_permissions = serializers.SerializerMethodField()
    scouts_groups = serializers.SerializerMethodField()
    scouts_functions = serializers.SerializerMethodField()

    class Meta:
        model = ScoutsUser
        exclude = ["password", "persisted_scouts_groups", "persisted_scouts_functions"]

    def get_user_permissions(self, obj: ScoutsUser):
        return obj.permissions

    def get_scouts_groups(self, obj: ScoutsUser) -> List[dict]:
        groups: List[ScoutsGroup] = [
            group
            for group in obj.persisted_scouts_groups.all()
            if obj.has_role_leader(group=group)
            or obj.has_role_district_commissioner(group=group)
        ]

        if obj.has_role_district_commissioner():
            district_commissioner_groups = obj.get_district_commissioner_groups()

            groups: List[ScoutsGroup] = ListUtils.concatenate_unique_lists(
                groups, district_commissioner_groups
            )

            groups.sort(key=lambda group: group.group_admin_id)

        return [
            {
                "group_admin_id": group.group_admin_id,
                "name": group.name,
                "full_name": group.full_name,
                "type": group.group_type,
                "is_section_leader": obj.has_role_section_leader(group=group),
                "is_group_leader": obj.has_role_group_leader(group=group),
                "is_district_commissioner": obj.has_role_district_commissioner(
                    group=group
                ),
            }
            for group in groups
        ]

    def get_scouts_functions(self, obj: ScoutsUser) -> List[dict]:
        return [
            {
                "group_admin_id": function.group_admin_id,
                "scouts_groups": [
                    group.group_admin_id for group in function.scouts_groups.all()
                ],
                "code": function.code,
                "description": function.description,
                "is_leader": function.is_leader(),
                "is_group_leader": function.is_group_leader(),
                "is_district_commissioner": function.is_district_commissioner(),
                "end": function.end,
            }
            for function in obj.persisted_scouts_functions.all()
        ]

    def to_internal_value(self, data: dict) -> dict:
        group_admin_id = data.get("group_admin_id", None)
        if group_admin_id:
            return ScoutsUser.objects.safe_get(
                group_admin_id=group_admin_id, raise_error=True
            )

        return super().to_internal_value(data)
