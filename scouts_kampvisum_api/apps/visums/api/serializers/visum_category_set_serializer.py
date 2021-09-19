from rest_framework import serializers

from ..models import LinkedCategorySet
from ..serializers import CategorySetAPISerializer
from inuits.mixins import FlattenMixin


class LinkedCategorySetAPISerializer(FlattenMixin, serializers.ModelSerializer):
    class Meta:
        model = LinkedCategorySet
        fields = []
        flatten = [("origin", CategorySetAPISerializer)]
