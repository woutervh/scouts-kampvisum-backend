import logging

from rest_framework import serializers

from apps.people.models import InuitsMember


logger = logging.getLogger(__name__)


class InuitsMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = InuitsMember
        fields = "__all__"

    def validate(self, data: dict) -> InuitsMember:
        logger.debug("INUITS MEMBER SERIALIZER DATA: %s", data)
        return InuitsMember(**data)
