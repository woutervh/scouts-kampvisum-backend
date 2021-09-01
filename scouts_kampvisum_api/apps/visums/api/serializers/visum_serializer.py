from rest_framework import serializers

from ..models import CampVisum
from ..serializers import CategorySetSerializer
from apps.camps.serializers import CampAPISerializer
from inuits.mixins import FlattenMixin


class CampVisumSerializer(FlattenMixin, serializers.ModelSerializer):

    # camp = CampAPISerializer()
    # category_set = CategorySetSerializer()

    class Meta:
        model = CampVisum
        fields = []
        flatten = [('camp', CampAPISerializer)]
