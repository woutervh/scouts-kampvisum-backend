import pytz

from rest_framework import serializers


class DateTimeTimezoneSerializerField(serializers.DateTimeField):
    """Class to make output of a DateTime Field timezone aware"""

    serialize = True

    def to_representation(self, value):
        if value and (not hasattr(value, "tzinfo") or value.tzinfo is None or value.tzinfo.utcoffset(value) is None):
            value = pytz.utc.localize(value)
        return super().to_representation(value)
