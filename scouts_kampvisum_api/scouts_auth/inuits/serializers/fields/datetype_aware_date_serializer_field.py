import logging
from datetime import datetime

from rest_framework import serializers


logger = logging.getLogger(__name__)


class DatetypeAwareDateSerializerField(serializers.DateField):
    serialize = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_internal_value(self, value):
        if value and isinstance(value, datetime):
            # logger.warn(
            #     "Field %s: Received a datetime value for a date field, transforming to date",
            #     self.field_name,
            # )
            value = value.date()
        return super().to_internal_value(value)

    def to_representation(self, value) -> datetime.date:
        if value and isinstance(value, datetime):
            # logger.warn(
            #     "Field %s: Attempting to serialize a datetime value for a date field, transforming into date",
            #     self.field_name,
            # )
            value = value.date()
        return super().to_representation(value)
