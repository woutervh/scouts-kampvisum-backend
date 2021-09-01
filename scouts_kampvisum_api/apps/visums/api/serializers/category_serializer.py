from rest_framework import serializers

from ..models import Category
from ..serializers import SubCategoryAPISerializer
from inuits.serializers.fields import OptionalCharField, RequiredIntegerField


class CategorySerializer(serializers.ModelSerializer):

    name = serializers.CharField(max_length=128)
    index = RequiredIntegerField()
    description = OptionalCharField()

    class Meta:
        model = Category()
        fields = "__all__"


class CampVisumCategoryAPISerializer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField()
    sub_categories = SubCategoryAPISerializer(many=True)

    class Meta:
        model = Category()
        fields = ["name", "uuid", "status", "sub_categories"]

    def get_status(self, obj):
        return False
