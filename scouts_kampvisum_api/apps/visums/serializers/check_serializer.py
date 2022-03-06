from rest_framework import serializers

from apps.visums.models import Check
from apps.visums.serializers import CheckTypeSerializer


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CheckSerializer(serializers.ModelSerializer):

    # sub_category = SubCategorySerializer()
    check_type = CheckTypeSerializer()

    class Meta:
        model = Check
        # fields = "__all__"
        exclude = ["sub_category", "change_handler"]

    def to_internal_value(self, data: dict) -> dict:
        logger.debug("CHECK SERIALIZER TO_INTERNAL_VALUE: %s", data)

        id = data.get("id", None)
        if id:
            instance: Check = Check.objects.safe_get(**data)
            if instance:
                data = {
                    "id": id,
                    "name": instance.name,
                    "check_type": {
                        "id": instance.check_type.id,
                        "check_type": instance.check_type.check_type,
                    },
                }
        logger.debug("CHECK SERIALIZER TO_INTERNAL_VALUE: %s", data)

        data = super().to_internal_value(data)
        logger.debug("CHECK SERIALIZER TO_INTERNAL_VALUE: %s", data)
        data["id"] = id

        return data

    def validate(self, data: dict) -> Check:
        return Check.objects.safe_get(**data, raise_error=True)
