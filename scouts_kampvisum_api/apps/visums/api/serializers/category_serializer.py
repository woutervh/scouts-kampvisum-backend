from rest_framework import serializers

from ..models import Category
from inuits.serializers.fields import OptionalCharField, RequiredIntegerField


class CategorySerializer(serializers.ModelSerializer):

    name = serializers.CharField(max_length=128)
    index = RequiredIntegerField()
    description = OptionalCharField()

    class Meta:
        model = Category()
        fields = '__all__'
