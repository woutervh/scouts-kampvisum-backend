from rest_framework import serializers

from scouts_auth.groupadmin.models import ScoutsUser


class ScoutsUserSerializer(serializers.ModelSerializer):

    user_permissions = serializers.SerializerMethodField()
    scouts_groups = serializers.SerializerMethodField()
    functions = serializers.SerializerMethodField()

    class Meta:
        model = ScoutsUser
        exclude = ["password"]

    def get_user_permissions(self, obj: ScoutsUser):
        return obj.permissions

    def get_scouts_groups(self, obj: ScoutsUser):
        return [
            {
                "group_admin_id": group.group_admin_id,
                "name": group.name,
                "full_name": group.full_name,
                "type": group.type,
            }
            for group in obj.scouts_groups
        ]

    def get_functions(self, obj: ScoutsUser):
        return [
            {
                "type": function.type,
                "function": function.function,
                "scouts_group": function.scouts_group.group_admin_id,
                "code": function.code,
                "description": function.description,
            }
            for function in obj.functions
        ]
