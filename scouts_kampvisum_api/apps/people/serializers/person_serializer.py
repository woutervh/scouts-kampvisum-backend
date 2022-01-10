from rest_framework import serializers

from apps.people.models import Person


class PersonSerializer(serializers.Serializer):
    class Meta:
        model = Person
        fields = "__all__"
