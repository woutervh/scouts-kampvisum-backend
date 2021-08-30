from rest_framework import serializers

from ..models import CampVisumCategory
from inuits.serializers.fields import OptionalCharField, RequiredIntegerField


class CampVisumCategorySerializer(serializers.ModelSerializer):

    name = serializers.CharField(max_length=128)
    index = RequiredIntegerField()
    description = OptionalCharField()

    class Meta:
        model = CampVisumCategory()
        fields = '__all__'
