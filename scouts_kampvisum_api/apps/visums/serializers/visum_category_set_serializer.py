from rest_framework import serializers

from apps.visums.models import LinkedCategorySet
from apps.visums.serializers import CategorySetAPISerializer

from scouts_auth.inuits.mixins import FlattenSerializerMixin


class LinkedCategorySetAPISerializer(
    FlattenSerializerMixin, serializers.ModelSerializer
):
    class Meta:
        model = LinkedCategorySet
        fields = []
        flatten = [("origin", CategorySetAPISerializer)]
