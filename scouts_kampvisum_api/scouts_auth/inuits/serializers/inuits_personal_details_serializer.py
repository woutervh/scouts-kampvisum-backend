import logging

from rest_framework import serializers

from scouts_auth.inuits.models import InuitsPersonalDetails
from scouts_auth.inuits.serializers import DatetypeAwareDateSerializerField


logger = logging.getLogger(__name__)


class InuitsPersonalDetailsSerializer(serializers.Serializer):
    # first_name    max_length=15           required
    # last_name     max_length=25           required
    # phone_number  max_length=24           optional
    # cell_number   max_length=24           optional
    # email         EmailField              optional
    # birth_date    date                    optional
    # gender        choices=Gender.choices  optional
    birth_date = DatetypeAwareDateSerializerField(required=False)

    class Meta:
        model = InuitsPersonalDetails
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
