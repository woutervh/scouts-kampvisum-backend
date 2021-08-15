from django.db import models
from django.utils import timezone
from rest_framework import serializers

from ....base.models import RecursiveField
from .models import ScoutsGroupType, ScoutsLocation, ScoutsAddress, ScoutsGroup


class ScoutsGroupTypeSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutsGroupType object.
    """
    
    type = models.CharField(max_length=64)
    
    class Meta:
        model = ScoutsGroupType
        fields = '__all__'
    
    def create(self, validated_data) -> ScoutsGroupType:
        return ScoutsGroupType(**validated_data)
    
    def update(self, instance, validated_data) -> ScoutsGroupType:
        instance.type = validated_data.get('type', instance.type)
        
        return type


class ScoutsLocationSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutsLocation object.
    """
    
    latitude = models.CharField(default='')
    longitude = models.CharField(default='')
    
    class Meta:
        model = ScoutsLocation
        fields = '__all__'
    
    def create(self, validated_data)-> ScoutsLocation:
        return ScoutsLocation(**validated_data)
    
    def update(self, instance, validated_data) -> ScoutsLocation:
        instance.latitude = validated_data.get(
            'latitude', instance.latitude)
        instance.longitude = validated_data.get(
            'longitude', instance.longitude)
        
        return instance


class GroupAdminAddressSerializer(serializers.Serializer):
    """
    Serializes an address from GroupAdmin.
    """
    
    group_admin_id = serializers.CharField(source='id', default='')
    country = serializers.CharField(source='land', default='')
    postalCode = serializers.CharField(source='postcode', default='')
    city = serializers.CharField(source='gemeente', default='')
    street = serializers.CharField(source='straat', default='')
    number = serializers.CharField(source='nummer', default='')
    box = serializers.CharField(source='bus', default='')
    phone = serializers.CharField(source='telefoon', default='')
    postalAddress = serializers.BooleanField(
        source='postadres', default=False)
    status = serializers.CharField(default='')
    location = ScoutsLocationSerializer(source='positie', default=None)
    description = serializers.CharField(source='omschrijving', default='')


class GroupAdminGroupSerializer(serializers.Serializer):
    """
    Serializes a group from GroupAdmin.
    """
    
    group_admin_id = serializers.CharField(source='id', default='')
    number = serializers.CharField(source='groepsnummer', default='')
    name = serializers.CharField(source='naam', default='')
    addresses = GroupAdminAddressSerializer(
        source='adressen', default=list(), many=True)
    foundation = serializers.DateTimeField(
        source='opgericht', default=timezone.now)
    only_leaders = serializers.BooleanField(
        source='enkelLeiding', default=False)
    show_members_improved = serializers.BooleanField(
        source='ledenVerbeterdTonen', default=False)
    email = serializers.CharField(default='')
    website = serializers.CharField(default='')
    info = serializers.CharField(source='vrijeInfo')
    sub_groups = RecursiveField(
        source='onderliggendeGroepen', default=list(), many=True)
    group_type = serializers.CharField(source='soort', default='')
    public_registration = serializers.BooleanField(
        source='publiek-inschrijven', default=False)


class ScoutsAddressSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutsAddress object.
    """
    
    # id
    group_admin_id = serializers.CharField()
    # land
    country = serializers.CharField()
    # postcode
    postalCode = serializers.CharField()
    # gemeente
    city = serializers.CharField()
    # straat
    street = serializers.CharField()
    # nummer
    number = serializers.CharField()
    # bus
    bus = serializers.CharField()
    # telefoon
    phone = serializers.CharField()
    # postadres
    postalAddress = serializers.BooleanField()
    # status
    status = serializers.CharField()
    # email
    email = serializers.CharField()
    # positie
    location = ScoutsLocationSerializer()
    # omschrijving
    description = serializers.CharField()
    
    class Meta:
        model = ScoutsAddress
        fields = '__all__'
    
    def create(self, validated_data) -> ScoutsAddress:
        return ScoutsAddress(**validated_data)
    
    def update(self, instance, validated_data) -> ScoutsAddress:
        instance.id = validated_data.get(
            'id', instance.id)
        instance.country = validated_data.get(
            'land', instance.id)
        instance.postal_code = validated_data.get(
            'postcode', instance.postal_code)
        instance.city= validated_data.get('gemeente', instance.city)
        instance.street = validated_data.get('straat', instance.street)
        instance.number = validated_data.get('nummer', instance.number)
        instance.box = validated_data.get('bus', instance.box)
        instance.phone = validated_data.get('telefoon', instance.phone)
        instance.postal_address = validated_data.get(
            'postadres', instance.postal_address)
        instance.status = validated_data.get('status', instance.status)
        instance.position = ScoutsLocationSerializer(source='positie')
        instance.description = validated_data(
            'omschrijving', instance.description)
        
        return instance


class ScoutsGroupSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutGroup object.
    """
    
    type = ScoutsGroupTypeSerializer()
    name = serializers.CharField()
    location = serializers.CharField()
    uuid = serializers.UUIDField()
    
    class Meta:
        model = ScoutsGroup
        fields = '__all__'
    
    def create(self, validated_data) -> ScoutsGroup:
        return ScoutsGroup(**validated_data)
    
    def update(self, instance, validated_data) -> ScoutsGroup:
        instance.type = ScoutsGroupType.objects.get(type='Scouts')
        instance.group_admin_id = validated_data.get(
            'id', instance.group_admin_id)
        instance.number = validated_data.get(
            'groepsnummer', instance.number)
        instance.name = validated_data.get(
            'naam', instance.name)
        instance.addresses = ScoutsAddressSerializer(many=True)
        instance.foundation = validated_data.get(
            'opgericht', instance.foundation)
        instance.only_leaders = validated_data.get(
            'enkelLeiding', instance.only_leaders)
        instance.show_members_improved = validated_data.get(
            'ledenVerbeterdTonen', instance.show_members_improved)
        instance.email = validated_data.get('email', instance.email)
        instance.website = validated_data.get('website', instance.website)
        instance.info = validated_data.get('vrijeInfo', instance.info)
        instance.sub_groups = ScoutsGroupSerializer(many=True)
        instance.group_type = validated_data.get('soort', instance.group_type)
        instance.public_registration = validated_data.get(
            'publiek-inschrijven', instance.public_registration)
        
        return instance

