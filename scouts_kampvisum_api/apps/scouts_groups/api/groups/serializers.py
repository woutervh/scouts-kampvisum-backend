import uuid
from django.db import models
from rest_framework import serializers

from .models import ScoutsGroupType, ScoutsGroup


class ScoutsGroupTypeSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutsGroupType object.
    """
    
    type = models.CharField(max_length=64)
    
    class Meta:
        model = ScoutsGroupType
        fields = '__all__'


class ScoutsGroupSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutGroup object.
    """
    
    type = ScoutsGroupTypeSerializer()
    id = models.AutoField(
        primary_key=True, editable=False)
    name = models.CharField(
        max_length=128)
    location = models.CharField(
        max_length=128)
    uuid = models.UUIDField(
        primary_key=False, default=uuid.uuid4(), editable=False, unique=True)
    
    class Meta:
        model = ScoutsGroup
        fields = '__all__'

