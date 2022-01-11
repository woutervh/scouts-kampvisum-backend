from rest_framework import serializers

from apps.people.models import InuitsMember


class InuitsMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = InuitsMember
        fields = "__all__"
