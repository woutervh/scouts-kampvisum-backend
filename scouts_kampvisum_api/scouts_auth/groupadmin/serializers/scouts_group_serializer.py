from rest_framework import serializers

from scouts_auth.groupadmin.models import ScoutsGroup


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoutsGroup
        fields = "__all__"

    def validate(self, data: dict) -> ScoutsGroup:
        logger.debug("SCOUTS GROUP SERIALIZER VALIDATE: %s", data)
        group = ScoutsGroup.objects.safe_get(group_admin_id=data.get("group_admin_id"))

        if group:
            return group

        return ScoutsGroup(**data)
