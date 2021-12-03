from rest_framework import serializers

from ..models import CategorySetPriority


class CategorySetPrioritySerializer(serializers.ModelSerializer):

    owner = serializers.CharField(max_length=32, default="Verbond")
    priority = serializers.IntegerField(default=100)

    class Meta:
        model = CategorySetPriority
        fields = "__all__"
