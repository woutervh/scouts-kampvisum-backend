from django.db import models
from rest_framework import serializers


class SetupItem:

    ok = False
    endpoint = ''
    objects = ()

    def __init__(self, ok=False, endpoint='') -> None:
        self.ok = ok
        self.endpoint = endpoint

    def status(self):
        return self.ok
    
    def add_object(self, object):
        self.objects.push(object)
    
    def add_objects(self, objects):
        for object in objects:
            self.objects.push(object)
    
    def count_objects(self, objects):
        return len(self.objects)


class Setup:

    global_status = False
    endpoint = '/api/setup/init'
    groups = SetupItem(endpoint='/api/groups/import')
    sections = SetupItem()

    def __init__(self) -> None:
        self.global_status()

    def global_status(self):
        if self.check_groups() and self.check_sections():
            self.global_status = True
        else:
            self.global_status = False
        
        return self.global_status

    def check_groups(self):
        self.groups.ok = True

        return self.groups.ok
    
    def check_sections(self):
        self.sections.ok = True

        return self.groups.ok


class SetupItemSerializer(serializers.Serializer):
    """
    Serializes a setup item.
    """

    ok = serializers.BooleanField(default=False)
    endpoint = serializers.CharField(default='')


class SetupSerializer(serializers.Serializer):
    """
    Serializes setup information.
    """
    
    global_status = serializers.BooleanField(default=False)
    endpoint = serializers.CharField(default='')
    groups = SetupItemSerializer()
    sections = SetupItemSerializer()

