from django.db import models
from django.utils import timezone
from rest_framework import serializers

from ..base.models import RecursiveField
from .api import GroupAdminApi


class GroupAdminLocationSerializer(serializers.Serializer):
    """
    Serializes a geolocation from GroupAdmin.
    """
    
    latitude = serializers.CharField(default='')
    longitude = serializers.CharField(default='')


class GroupAdminAddressSerializer(serializers.Serializer):
    """
    Serializes an address from GroupAdmin.
    """
    
    group_admin_uuid = serializers.CharField(source='id', default='')
    country = serializers.CharField(source='land', default='')
    postal_code = serializers.CharField(source='postcode', default='')
    city = serializers.CharField(source='gemeente', default='')
    street = serializers.CharField(source='straat', default='')
    number = serializers.CharField(source='nummer', default='')
    box = serializers.CharField(source='bus', default='')
    phone = serializers.CharField(source='telefoon', default='')
    postal_address = serializers.BooleanField(
        source='postadres', default=False)
    status = serializers.CharField(default='')
    location = GroupAdminLocationSerializer(source='positie', default=None)
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
    group_type = serializers.CharField(
        source='soort', default=GroupAdminApi.default_scouts_group_type)
    public_registration = serializers.BooleanField(
        source='publiek-inschrijven', default=False)

