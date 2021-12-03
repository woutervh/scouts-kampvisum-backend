from rest_framework import serializers

from ..models import CampVisum
from ..serializers import (
    LinkedCategorySetAPISerializer,
)
from apps.camps.serializers import CampAPISerializer
from inuits.mixins import FlattenMixin


class CampVisumSerializer(FlattenMixin, serializers.ModelSerializer):
    class Meta:
        model = CampVisum
        fields = ["uuid"]
        flatten = [
            ("camp", CampAPISerializer),
            ("category_set", LinkedCategorySetAPISerializer),
        ]
