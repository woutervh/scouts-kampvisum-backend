import logging

from rest_framework import serializers

from apps.people.models import InuitsNonMember


logger = logging.getLogger(__name__)


class InuitsNonMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = InuitsNonMember
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        logger.debug("DATA: %s", data)
        # If the data dict contains an id, assume it's simple object input
        if data.get("id", None):
            instance = InuitsNonMember.objects.safe_get(pk=id)
            logger.debug("instance: %s", instance)
            if instance:
                return instance
        data = super().to_internal_value(data)
        logger.debug("DATA: %s", data)

        return data

    def validate(self, data: dict) -> InuitsNonMember:
        logger.debug("DATA: %s", data)

        return InuitsNonMember(**data)
