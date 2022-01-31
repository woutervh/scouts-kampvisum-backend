from rest_framework import serializers

from apps.visums.models import SubCategory


class SubCategorySerializer(serializers.ModelSerializer):

    name = serializers.CharField(max_length=128)

    class Meta:
        model = SubCategory
        fields = "__all__"


class SubCategoryAPISerializer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField()

    class Meta:
        model = SubCategory
        fields = ["name", "id", "status"]

    def get_status(self, obj):
        return False
