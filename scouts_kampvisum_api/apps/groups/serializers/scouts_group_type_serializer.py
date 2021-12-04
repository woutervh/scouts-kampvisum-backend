from rest_framework import serializers

from apps.groups.models import ScoutsGroupType

from scouts_auth.inuits.serializers.fields import RecursiveSerializerField


class ScoutsGroupTypeSerializer(serializers.ModelSerializer):
    """
    Serializes a GroupType object.
    """

    parent = RecursiveSerializerField()

    class Meta:
        model = ScoutsGroupType
        fields = "__all__"
