from rest_framework import serializers

from apps.visums.models import CampVisum
from apps.visums.serializers import CategorySetAPISerializer
from apps.camps.serializers import CampAPISerializer

from scouts_auth.inuits.mixins import FlattenSerializerMixin


class CampVisumSerializer(FlattenSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = CampVisum
        fields = ["uuid"]
        flatten = [
            ("camp", CampAPISerializer),
            ("category_set", CategorySetAPISerializer),
        ]
