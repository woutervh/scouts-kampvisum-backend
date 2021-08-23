from django.db import models
from django.utils import timezone
from rest_framework import serializers

from apps.base.models import RecursiveField
from apps.groupadmin.api import GroupAdminApi
from ..models import ScoutsGroupType


class ScoutsGroupTypeSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutsGroupType object.
    """
    
    type = models.CharField(
        max_length=64, default=GroupAdminApi.default_scouts_group_type)
    parent = RecursiveField()
    
    class Meta:
        model = ScoutsGroupType
        fields = '__all__'
    
    def create(self, validated_data) -> ScoutsGroupType:
        return ScoutsGroupType(**validated_data)
    
    def update(self, instance, validated_data) -> ScoutsGroupType:
        instance.type = validated_data.get('type', instance.type)
        instance.parent = validated_data.get('parent', instance.parent)
        
        return type

