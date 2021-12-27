import logging

from rest_framework import serializers


logger = logging.getLogger(__name__)


class EnumSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()

    def get_id(self, obj):
        # Set id equal to value to make it easier for clients
        return self.get_value(obj)

    def get_value(self, obj):
        logger.debug("OBJ ENUM: %s", obj)
        # Value of enum is 0 of tuple
        return obj[0]

    def get_label(self, obj):
        logger.debug("OBJ ENUM: %s", obj)
        # Label of enum is 1 of tuple
        return obj[1]
