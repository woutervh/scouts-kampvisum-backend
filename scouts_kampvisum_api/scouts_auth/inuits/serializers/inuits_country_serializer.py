import logging

from scouts_auth.inuits.models import InuitsCountry
from scouts_auth.inuits.serializers import NonModelSerializer


logger = logging.getLogger(__name__)


class InuitsCountrySerializer(NonModelSerializer):
    # name          max_length=64       required
    # code          max_length=2        optional

    class Meta:
        model = InuitsCountry
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
