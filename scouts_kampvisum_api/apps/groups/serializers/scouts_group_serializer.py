from apps.groups.models import ScoutsGroup
from apps.groups.serializers import ScoutsGroupTypeSerializer

from scouts_auth.groupadmin.serializers import AbstractScoutsGroupSerializer


class ScoutsGroupSerializer(AbstractScoutsGroupSerializer):
    """
    Serializes a ScoutGroup object.
    """

    type = ScoutsGroupTypeSerializer()

    class Meta:
        model = ScoutsGroup
        fields = "__all__"
