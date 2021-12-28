import logging
from datetime import date, datetime

from rest_framework import serializers


logger = logging.getLogger(__name__)


class NonModelSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_attribute(self, instance, attribute_name):
        # logger.debug("Getting attribute %s for instance of %s", attribute_name, instance.__class__.__name__)
        if hasattr(instance, attribute_name):
            attribute = getattr(instance, attribute_name)
            # logger.debug("Found attribute: %s", attribute)

            return attribute

        return None

    def get_object():
        raise NotImplementedError("The get_object method should be implemented in a concrete subclass.")

    def to_internal_value(self, data):

        # Attempt to
        try:
            # logger.debug("NON-MODEL: deserializing data: %s", data)
            validated_data = super().to_internal_value(data)
            # logger.debug("NON-MODEL: deserialized data: %s", validated_data)

            return validated_data
        except Exception:
            """NonModelSerializer instances must implement this to support read operations."""
            raise NotImplementedError("The to_internal_value method should be implemented in a concrete subclass.")

    def to_representation(self, instance):
        """
        BaseSerializer instances must implement this to support write operations.

        @see https://www.django-rest-framework.org/api-guide/serializers/#creating-new-base-classes
        """
        # logger.debug("Serializing instance of type %s", instance.__class__.__name__)

        output = {}
        for attribute_name in dir(instance):
            if attribute_name == "pk":
                # Ignore keys on abstract models
                continue

            attribute = self._get_attribute(instance, attribute_name)
            if attribute_name.startswith("_"):
                # Ignore private attributes.
                pass
            elif hasattr(attribute, "__call__"):
                # Ignore methods and other callables.
                pass
            elif isinstance(attribute, type(None)):
                # Ignore attributes that were set to None in the serializers
                pass
            elif isinstance(attribute, str):
                # Ignore empty strings
                if len(attribute) > 0:
                    # logger.debug("Serializing string attribute %s as %s", attribute_name, attribute)
                    output[attribute_name] = attribute
            elif isinstance(attribute, (int, float, bool)):
                # logger.debug("Serializing primitive attribute %s as %s", attribute_name, attribute)
                # Primitive types can be passed through unmodified.
                output[attribute_name] = attribute
            elif isinstance(attribute, list):
                # Ignore lists that contain no elements
                if len(attribute) > 0:
                    # logger.debug("Serializing list attribute %s", attribute_name)
                    # logger.debug("List contents: %s", attribute)
                    # Recursively deal with items in lists.
                    output[attribute_name] = [NonModelSerializer().to_representation(item) for item in attribute]
            elif isinstance(attribute, dict):
                # Ignore empty dictionaries
                if len(attribute.keys()) > 0:
                    # logger.debug("Serializing dict attribute %s", attribute_name)
                    # Recursively deal with items in dictionaries.
                    output[attribute_name] = {
                        str(key): NonModelSerializer().to_representation(value) for key, value in attribute.items()
                    }
            elif isinstance(attribute, date) or isinstance(attribute, datetime):
                # logger.debug("Serializing datetime attribute %s", attribute_name)
                output[attribute_name] = str(attribute)
            elif hasattr(attribute, "__class__"):
                # logger.debug("Serializing nested class attribute %s", attribute_name)
                output[attribute_name] = NonModelSerializer().to_representation(attribute)
            else:
                # Force anything else to its string representation.
                output[attribute_name] = str(attribute)

        return output
