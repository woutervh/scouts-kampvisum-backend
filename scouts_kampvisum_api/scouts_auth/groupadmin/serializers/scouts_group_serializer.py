from rest_framework import serializers

from scouts_auth.groupadmin.models import ScoutsGroup


class ScoutsGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoutsGroup
        fields = "__all__"
