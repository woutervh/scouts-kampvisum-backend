from rest_framework import serializers

from apps.people.models import InuitsNonMember


class InuitsNonMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = InuitsNonMember
        fields = "__all__"

    def validate(self, data: dict) -> InuitsNonMember:
        return InuitsNonMember(**data)
