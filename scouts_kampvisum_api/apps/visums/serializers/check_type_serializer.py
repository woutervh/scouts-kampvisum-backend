from rest_framework import serializers

from apps.visums.models import CheckType, CheckTypeEnum


class CheckTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckType
        fields = "__all__"

    # HACKETY-HACK
    def to_representation(self, obj: CheckType) -> dict:
        data = super().to_representation(obj)

        if (
            obj.is_participant_member_check()
            or obj.is_participant_cook_check()
            or obj.is_participant_leader_check()
            or obj.is_participant_responsible_check()
            or obj.is_participant_adult_check()
        ):
            data["check_type"] = CheckTypeEnum.PARTICIPANT_CHECK

        return data
