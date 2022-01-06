import logging

from rest_framework import serializers

from apps.camps.serializers import (
    CampSerializer,
    CampAPISerializer,
)
from apps.visums.models import CampVisum
from apps.visums.serializers import (
    LinkedCategorySetSerializer,
    CategorySetAPISerializer,
)

from scouts_auth.inuits.mixins import FlattenSerializerMixin


logger = logging.getLogger(__name__)


class CampVisumSerializer(FlattenSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = CampVisum
        fields = ["id"]
        flatten = [
            ("camp", CampSerializer),
            ("category_set", LinkedCategorySetSerializer),
        ]

    def to_internal_value(self, data: dict) -> dict:
        logger.debug("SERIALIZER TO INTERNAL VALUE: %s", data)

        return super().to_internal_value(data)
