from rest_framework import serializers

from scouts_auth.inuits.models import InuitsPerson
from scouts_auth.inuits.serializers import InuitsPersonalDetailsSerializer, InuitsAddressSerializer


class InuitsPersonSerializer(InuitsPersonalDetailsSerializer, InuitsAddressSerializer, serializers.ModelSerializer):
    class Meta:
        model = InuitsPerson
        fields = "__all__"
