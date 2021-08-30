from rest_framework import serializers

from ..models import CampVisumCategorySetPriority


class CampVisumCategorySetPrioritySerializer(serializers.ModelSerializer):

    owner = serializers.CharField(max_length=32, default='Verbond')
    priority = serializers.IntegerField(default=100)

    class Meta:
        model = CampVisumCategorySetPriority
        fields = '__all__'
