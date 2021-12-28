import logging

from rest_framework import serializers

from scouts_auth.inuits.models import InuitsAddress


logger = logging.getLogger(__name__)


class InuitsAddressSerializer(serializers.Serializer):
    # street        max_length=100          optional
    # number        max_length=5            optional
    # letter_box    max_length=5            optional
    # postal_code   number                  optional
    # city          max_length=40           optional
    # country       InuitsCountry           optional

    class Meta:
        model = InuitsAddress
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
