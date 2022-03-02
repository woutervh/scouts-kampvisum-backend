from rest_framework import serializers


import logging

logger = logging.getLogger(__name__)


class RecursiveSerializerField(serializers.Serializer):
    """
    Utility class that allows serialization of self-referencing classes.
    """

    cls = None

    def __init__(self, *args, **kwargs):
        cls = kwargs.get("cls", None)
        if cls:
            self.cls = cls

    def to_internal_value(self, data: dict) -> dict:
        logger.debug("self.parent: %s", self.parent)
        logger.debug("self.parent.parent: %s", self.parent.parent)
        logger.debug("self.parent.parent.__class__: %s", self.parent.parent.__class__)
        serializer = self.parent.parent.__class__()

    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)

        return serializer.data
