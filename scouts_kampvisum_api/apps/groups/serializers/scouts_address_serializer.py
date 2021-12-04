from apps.groups.models import ScoutsAddress
from apps.groups.serializers import ScoutsGroupSerializer

from scouts_auth.groupadmin.serializers import AbstractScoutsAddressSerializer


class ScoutsAddressSerializer(AbstractScoutsAddressSerializer):
    """
    Serializes a Address object.
    """

    group = ScoutsGroupSerializer()

    class Meta:
        model = ScoutsAddress
        fields = "__all__"
