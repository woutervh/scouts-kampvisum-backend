from rest_framework import serializers

from apps.visums.models import CategoryPriority


class CategoryPrioritySerializer(serializers.ModelSerializer):

    owner = serializers.CharField(max_length=32, default="Verbond")
    priority = serializers.IntegerField(default=100)

    class Meta:
        model = CategoryPriority
        fields = "__all__"
