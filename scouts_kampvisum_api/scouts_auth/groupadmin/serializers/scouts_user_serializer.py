from typing import List

from rest_framework import serializers

from scouts_auth.groupadmin.models import ScoutsUser
from scouts_auth.groupadmin.serializers import (
    ScoutsGroupSerializer,
    ScoutsFunctionSerializer,
)


class ScoutsUserSerializer(serializers.ModelSerializer):

    user_permissions = serializers.SerializerMethodField()
    # scouts_groups = serializers.SerializerMethodField()
    # functions = serializers.SerializerMethodField()
    # scouts_groups = ScoutsGroupSerializer(many=True, required=False)
    # scouts_functions = ScoutsFunctionSerializer(many=True, required=False)
    scouts_groups = serializers.SerializerMethodField()
    scouts_functions = serializers.SerializerMethodField()

    class Meta:
        model = ScoutsUser
        exclude = ["password", "persisted_scouts_groups", "persisted_scouts_functions"]

    def get_user_permissions(self, obj: ScoutsUser):
        return obj.permissions

    def get_scouts_groups(self, obj: ScoutsUser) -> List[dict]:
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
            for group in obj.persisted_scouts_groups.all()
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
            }
            for function in obj.persisted_scouts_functions.all()
        ]

    # def get_scouts_groups(self, obj: ScoutsUser):
    #     return [
    #         {
    #             "group_admin_id": group.group_admin_id,
    #             "name": group.name,
    #             "full_name": group.full_name,
    #             "type": group.type,
    #         }
    #         for group in obj.scouts_groups
    #     ]

    # def get_functions(self, obj: ScoutsUser):
    #     return [
    #         {
    #             "function": function.function,
    #             "scouts_group": function.scouts_group.group_admin_id,
    #             "code": function.code,
    #             "description": function.description,
    #         }
    #         for function in obj.functions
    # ]

    def to_internal_value(self, data: dict) -> dict:
        group_admin_id = data.get("group_admin_id", None)
        if group_admin_id:
            return ScoutsUser.objects.safe_get(
                group_admin_id=group_admin_id, raise_error=True
            )

        return super().to_internal_value(data)
