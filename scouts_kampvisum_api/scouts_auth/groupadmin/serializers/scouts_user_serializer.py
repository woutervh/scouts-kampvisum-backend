from rest_framework import serializers

from scouts_auth.groupadmin.models import ScoutsUser


class ScoutsUserSerializer(serializers.ModelSerializer):

    user_permissions = serializers.SerializerMethodField()
    scouts_groups = serializers.SerializerMethodField()

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
            }
            for group in obj.scouts_groups
        ]
