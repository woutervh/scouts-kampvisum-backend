from rest_framework import serializers

from scouts_auth.auth.models import User

from scouts_auth.groupadmin.serializers import AbstractScoutsGroupSerializer


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes a User instance into a string.
    """

    permissions = serializers.SerializerMethodField()
    birth_date = serializers.DateField()
    membership_number = serializers.CharField()
    phone_number = serializers.CharField()
    scouts_groups = AbstractScoutsGroupSerializer(many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "birth_date",
            "membership_number",
            "phone_number",
            "scouts_groups",
            "date_joined",
            "permissions",
            "group_admin_id",
        )

    def get_permissions(self, obj):
        return obj.get_all_permissions()
