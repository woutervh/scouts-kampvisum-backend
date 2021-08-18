from django.db import models
from django.utils import timezone
from rest_framework import serializers

from .models import ScoutsGroupType, ScoutsAddress, ScoutsGroup
from apps.base.models import RecursiveField
from apps.groupadmin.api import GroupAdminApi


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


class ScoutsGroupSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutGroup object.
    """
    
    group_admin_id = serializers.CharField(default='')
    number = serializers.CharField(default='')
    name = serializers.CharField(default='')
    foundation = serializers.DateTimeField(default=timezone.now)
    only_leaders = serializers.BooleanField(default=False)
    show_members_improved = serializers.BooleanField(default=False)
    email = serializers.CharField(default='')
    website = serializers.CharField(default='')
    info = serializers.CharField(default='')
    sub_groups = RecursiveField(default=list(), many=True)
    type = ScoutsGroupTypeSerializer()
    public_registration = serializers.BooleanField(default=False)
    
    class Meta:
        model = ScoutsGroup
        fields = '__all__'
    
    def create(self, validated_data) -> ScoutsGroup:
        return ScoutsGroup(**validated_data)
    
    def update(self, instance: ScoutsGroup, validated_data) -> ScoutsGroup:
        instance.group_admin_id = validated_data.get(
            'group_admin_id', instance.group_admin_id)
        instance.number = validated_data.get(
            'number', instance.number)
        instance.name = validated_data.get(
            'name', instance.name)
        instance.foundation = validated_data.get(
            'foundation', instance.foundation)
        instance.only_leaders = validated_data.get(
            'only_leaders', instance.only_leaders)
        instance.show_members_improved = validated_data.get(
            'show_members_improved', instance.show_members_improved)
        instance.email = validated_data.get('email', instance.email)
        instance.website = validated_data.get('website', instance.website)
        instance.info = validated_data.get('info', instance.info)
        instance.sub_groups = ScoutsGroupSerializer(many=True)
        instance.type = ScoutsGroupTypeSerializer()
        instance.public_registration = validated_data.get(
            'public_registration', instance.public_registration)
        
        return instance


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
    description = serializers.CharField()
    
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

