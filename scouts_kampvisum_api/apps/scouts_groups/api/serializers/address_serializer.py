from django.db import models
from django.utils import timezone
from rest_framework import serializers

from apps.base.models import RecursiveField
from apps.groupadmin.api import GroupAdminApi
from ..models import ScoutsGroupType, ScoutsAddress, ScoutsGroup
from ..serializers import ScoutsGroupSerializer
from inuits.serializers.fields import OptionalCharField


class ScoutsAddressSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutsAddress object.
    """
    
    group = ScoutsGroupSerializer()
    group_admin_uuid = serializers.CharField()
    country = serializers.CharField()
    postalCode = serializers.CharField()
    city = serializers.CharField()
    street = serializers.CharField()
    number = serializers.CharField()
    bus = serializers.CharField()
    phone = serializers.CharField()
    postalAddress = serializers.BooleanField()
    status = serializers.CharField()
    email = serializers.CharField()
    latitude = models.CharField(default='')
    longitude = models.CharField(default='')
    description = OptionalCharField()
    
    class Meta:
        model = ScoutsAddress
        fields = '__all__'
    
    def create(self, validated_data) -> ScoutsAddress:
        return ScoutsAddress(**validated_data)
    
    def update(self, instance, validated_data) -> ScoutsAddress:
        instance.group = ScoutsGroupSerializer(source='addressen')
        instance.group_admin_uuid = validated_data.get('id', instance.id)
        instance.country = validated_data.get(
            'country', instance.id)
        instance.postal_code = validated_data.get(
            'postal_code', instance.postal_code)
        instance.city= validated_data.get('city', instance.city)
        instance.street = validated_data.get('street', instance.street)
        instance.number = validated_data.get('number', instance.number)
        instance.box = validated_data.get('box', instance.box)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.postal_address = validated_data.get(
            'postal_address', instance.postal_address)
        instance.status = validated_data.get('status', instance.status)
        
        position_data = validated_data.get('position')
        if position_data:
            instance.latitude = position_data.get(
                'latitude', instance.latitude)
            instance.longitude = position_data.get(
                'longitude', instance.longitude)
        
        instance.description = validated_data(
            'description', instance.description)
        
        return instance

