import logging

from rest_framework import serializers

from apps.visums.models import LinkedCheck
from apps.visums.serializers import VisumCheckSerializer
from apps.visums.urls import LinkedCheckEndpointFactory


logger = logging.getLogger(__name__)


class LinkedCheckSerializer(serializers.ModelSerializer):

    parent = VisumCheckSerializer()
    endpoint = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    class Meta:
        model = LinkedCheck
        exclude = ["sub_category"]

    def get_endpoint(self, obj: LinkedCheck):
        return LinkedCheckEndpointFactory.get_endpoint(
            "{}/{}/".format(obj.parent.check_type.endpoint_route, obj.id)
        )

    def get_value(self, obj: LinkedCheck):
        if not hasattr(obj, "value"):
            logger.debug("LinkedCheck object has no value: %s", str(obj))
            return None

        value = obj.value
        logger.debug("LinkedCheck value: %s", value, type(value).__name__)
