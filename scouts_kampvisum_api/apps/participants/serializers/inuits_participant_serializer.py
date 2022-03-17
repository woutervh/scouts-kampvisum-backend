from rest_framework import serializers

from apps.participants.models import InuitsParticipant

from scouts_auth.groupadmin.models import AbstractScoutsMember
from scouts_auth.groupadmin.services import GroupAdminMemberService


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class InuitsParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = InuitsParticipant
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        # logger.debug("PARTICIPANT SERIALIZER TO INTERNAL VALUE: %s", data)

        group_admin_id = data.get("group_admin_id", None)
        id = data.get("id", None)
        group_group_admin_id = data.get("group_group_admin_id", None)
        email = data.get("email", None)

        participant = InuitsParticipant.objects.safe_get(
            id=id,
            group_admin_id=group_admin_id,
            group_group_admin_id=group_group_admin_id,
            email=email,
        )

        data = super().to_internal_value(data)

        if participant:
            data["id"] = participant.id

        return data

    def validate(self, data: any) -> InuitsParticipant:
        if isinstance(data, InuitsParticipant):
            return data

        return InuitsParticipant(**data)
