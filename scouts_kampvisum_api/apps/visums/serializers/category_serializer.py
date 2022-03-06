from rest_framework import serializers

from apps.visums.models import Category

from scouts_auth.inuits.serializers.fields import (
    OptionalCharSerializerField,
    RequiredIntegerSerializerField,
)


class CategorySerializer(serializers.ModelSerializer):

    name = serializers.CharField(max_length=128)
    index = RequiredIntegerSerializerField()
    description = OptionalCharSerializerField()

    class Meta:
        model = Category
        fields = "__all__"
