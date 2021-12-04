import logging

from django.core.exceptions import ValidationError
from rest_framework import serializers


logger = logging.getLogger(__name__)


class ChoiceSerializerField:
    instance = None

    CHOICE_FIELD = "ChoiceField"
    MULTIPLE_CHOICE_FIELD = "MultipleChoiceField"

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop("choices", None)
        source = kwargs.pop("source", None)
        many = kwargs.pop("many", False)

        if not choices:
            raise ValidationError("ChoiceSerializerField needs to have the choices field set")
        kwargs["choices"] = choices

        if source:
            kwargs["source"] = source

        parent = ChoiceSerializerField.CHOICE_FIELD
        if many:
            parent = ChoiceSerializerField.MULTIPLE_CHOICE_FIELD

        self.instance = getattr(serializers, parent)(*args, **kwargs)

    def bind(self, field_name, parent):
        logger.debug("FIELD NAME: %s", field_name)
        return self.instance.bind(field_name, parent)

    def get_value(self, dictionary):
        logger.debug("DICT: %s", dictionary)
        value = self.instance.get_value(dictionary)
        logger.debug("VALUE: %s", value)
        return value

    def to_internal_value(self, data):
        logger.debug("DATA: %s", data)
        return self.instance.to_internal_value(data)

    def to_representation(self, value):
        logger.debug("REPR: %s", value)
        return self.instance.to_representation(value)

    def validate(self, value):
        return self.instance.validate(value)
