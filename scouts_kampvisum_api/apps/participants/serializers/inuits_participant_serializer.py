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

    def to_internal_value(self, data: dict) -> any:
        logger.debug("PARTICIPANT SERIALIZER TO INTERNAL VALUE: %s", data)
        # If the data dict contains a group admin id, forget the rest and load the object from GA
        group_admin_id = data.get("group_admin_id", None)
        id = data.get("id", None)

        if group_admin_id:
            member: AbstractScoutsMember = GroupAdminMemberService().get_member_info(
                active_user=self.context.get("request").user,
                group_admin_id=group_admin_id,
            )

            if member:
                return InuitsParticipant.from_scouts_member(member)

        # If the data dict contains an id, assume it's simple object input
        if id and len(data.keys()) == 1:
            instance = InuitsParticipant.objects.safe_get(pk=id)
            if instance:
                return instance

        # Assume it's regular non-member create input
        data = super().to_internal_value(data)
        logger.debug("DATA: %s", data)

        return data
