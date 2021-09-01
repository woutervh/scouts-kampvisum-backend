from rest_framework import serializers

from ..models import SubCategory
from ..serializers import CategorySerializer


class SubCategorySerializer(serializers.ModelSerializer):

    category = CategorySerializer()
    name = serializers.CharField(max_length=128)

    class Meta:
        model = SubCategory()
        fields = "__all__"


class CampVisumSubCategoryAPISerializer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField()

    class Meta:
        model = SubCategory()
        fields = ["name", "uuid", "status"]

    def get_status(self, obj):
        return False
