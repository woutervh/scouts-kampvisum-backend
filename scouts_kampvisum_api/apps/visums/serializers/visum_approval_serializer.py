from rest_framework import serializers

from apps.visums.models import CampVisumApproval

from scouts_auth.groupadmin.serializers import ScoutsUserSerializer


class CampVisumApprovalSerializer(serializers.ModelSerializer):

    leaders = ScoutsUserSerializer(required=False)
    group_leaders = ScoutsUserSerializer(required=False)
    district_commissioner = ScoutsUserSerializer(required=False)

    class Meta:
        model = CampVisumApproval
        fields = "__all__"

    def to_representation(self, obj: CampVisumApproval) -> dict:
        data = super().to_representation(obj)

        data["can_sign"] = obj.can_sign()
        data["leaders_can_sign"] = obj.leaders_can_sign()
        data["group_leaders_can_sign"] = obj.group_leaders_can_sign()
        data["district_commissioner_can_sign"] = obj.district_commissioner_can_sign()

        return data
