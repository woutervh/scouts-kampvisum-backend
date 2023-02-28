from typing import List

from rest_framework import serializers

from scouts_auth.groupadmin.models import ScoutsUser, ScoutsGroup, ScoutsFunction
from scouts_auth.groupadmin.settings import GroupAdminSettings

from scouts_auth.inuits.utils import ListUtils


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsUserSerializer(serializers.ModelSerializer):

    groups = serializers.SerializerMethodField()
    user_permissions = serializers.SerializerMethodField()
    new_user_permissions = serializers.SerializerMethodField()
    scouts_groups = serializers.SerializerMethodField()
    scouts_functions = serializers.SerializerMethodField()

    class Meta:
        model = ScoutsUser
        exclude = ["password"]

    def get_groups(self, obj: ScoutsUser) -> List[str]:
        groups = obj.groups.all()
        return [group.name for group in groups]

    def get_user_permissions(self, obj: ScoutsUser) -> List:
        return obj.get_all_permissions()

    def get_new_user_permissions(self, obj: ScoutsUser) -> List[dict]:
        return []

    def get_scouts_groups(self, obj: ScoutsUser) -> List[dict]:
        return [
            {
                "group_admin_id": scouts_group.group_admin_id,
                "name": scouts_group.name,
                "full_name": scouts_group.full_name,
                "type": scouts_group.type,
                "is_section_leader": obj.has_role_section_leader(scouts_group=scouts_group),
                "is_group_leader": obj.has_role_group_leader(scouts_group=scouts_group),
                "is_district_commissioner": obj.has_role_district_commissioner(
                    scouts_group=scouts_group
                ),
                "is_shire_president": obj.has_role_shire_president(
                    scouts_group=scouts_group
                ),
                "is_admin": obj.has_role_administrator(),
            }
            for scouts_group in obj.get_scouts_leader_groups(include_underlying_groups=True)
        ]

    def get_scouts_functions(self, obj: ScoutsUser) -> List[dict]:
        return [
            {
                "group_admin_id": scouts_function.group_admin_id,
                "scouts_group": scouts_function.scouts_group,
                "code": scouts_function.code,
                "description": scouts_function.description,
                "is_leader": scouts_function.is_leader_function(),
                "is_section_leader": scouts_function.is_section_leader_function(),
                "is_group_leader": scouts_function.is_group_leader_function(),
                "is_district_commissioner": scouts_function.is_district_commissioner_function(),
                "is_shire_president": scouts_function.is_shire_president_function(),
                "end": scouts_function.end,
            }
            for scouts_function in obj.get_scouts_functions()
        ]

    def to_internal_value(self, data: dict) -> dict:
        group_admin_id = data.get("group_admin_id", None)
        if group_admin_id:
            return ScoutsUser.objects.safe_get(
                group_admin_id=group_admin_id, raise_error=True
            )

        return super().to_internal_value(data)
