from django.core.exceptions import ValidationError
from rest_framework import serializers

from apps.visums.models import CampVisumEngagement
from apps.visums.services import CampVisumEngagementService

from scouts_auth.groupadmin.serializers import ScoutsUserSerializer


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampVisumEngagementSerializer(serializers.ModelSerializer):

    leaders = ScoutsUserSerializer(required=False)
    group_leaders = ScoutsUserSerializer(required=False)
    district_commissioner = ScoutsUserSerializer(required=False)

    class Meta:
        model = CampVisumEngagement
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        id = data.get("id", None)

        data = super().to_internal_value(data)
        logger.debug("DATA: %s", data)

        if id:
            data["id"] = id if CampVisumEngagement.objects.safe_get(id=id) else None

        leaders = data.get("leaders", None)
        group_leaders = data.get("group_leaders", None)
        district_commissioner = data.get("district_commissioner", None)

        if not leaders:
            data["leaders"] = None
        if not group_leaders:
            data["group_leaders"] = None
        if not district_commissioner:
            data["district_commissioner"] = None

        return data

    def to_representation(self, obj: CampVisumEngagement) -> dict:
        logger.debug(f"CAMP VISUM ENGAGEMENT SERIALIZER TO_REPRESENTATION {obj}")
        data = super().to_representation(obj)
        logger.debug(f"CAMP VISUM ENGAGEMENT SERIALIZER TO_REPRESENTATION {obj}")

        data["can_sign"] = obj.can_sign()
        data["leaders_can_sign"] = obj.leaders_can_sign()
        data["group_leaders_can_sign"] = obj.group_leaders_can_sign()
        data["district_commissioner_can_sign"] = obj.district_commissioner_can_sign()

        if obj.leaders:
            data["leaders"] = {
                "id": obj.leaders.id,
                "first_name": obj.leaders.first_name,
                "last_name": obj.leaders.last_name,
                "email": obj.leaders.email,
                "group_admin_id": obj.leaders.group_admin_id,
                "username": obj.leaders.username,
            }
        if obj.group_leaders:
            data["group_leaders"] = {
                "id": obj.group_leaders.id,
                "first_name": obj.group_leaders.first_name,
                "last_name": obj.group_leaders.last_name,
                "email": obj.group_leaders.email,
                "group_admin_id": obj.group_leaders.group_admin_id,
                "username": obj.group_leaders.username,
            }
        if obj.district_commissioner:
            data["district_commissioner"] = {
                "id": obj.district_commissioner.id,
                "first_name": obj.district_commissioner.first_name,
                "last_name": obj.district_commissioner.last_name,
                "email": obj.district_commissioner.email,
                "group_admin_id": obj.district_commissioner.group_admin_id,
                "username": obj.district_commissioner.username,
            }

        logger.debug(f"CAMP VISUM ENGAGEMENT SERIALIZER TO_REPRESENTATION {data}")

        return data

    def validate(self, obj: any) -> any:
        if isinstance(obj, CampVisumEngagement):
            return obj

        if isinstance(obj, dict):
            engagement: CampVisumEngagement = None

            id = obj.get("id", None)
            leaders = obj.get("leaders", None)
            group_leaders = obj.get("group_leaders", None)
            district_commissioner = obj.get("district_commissioner", None)
            if id:
                engagement = CampVisumEngagement.objects.safe_get(
                    id=id, raise_error=True
                )

                leaders = engagement.leaders
                group_leaders = engagement.group_leaders
                district_commissioner = engagement.district_commissioner

            if (district_commissioner or group_leaders) and not leaders:
                raise ValidationError(
                    "Group leaders and DC's can only sign after the leaders have signed"
                )
            if district_commissioner and not (leaders or group_leaders):
                raise ValidationError(
                    "DC's can only sign after the leaders and group leaders have signed"
                )
            if district_commissioner and engagement:
                service = CampVisumEngagementService()

                if not service.is_signable_by_dc(
                    request=self.context.get("request"), instance=engagement
                ):
                    raise ValidationError(
                        "DC's can only sign if there are no sub-categories markes as DISAPPROVED"
                    )

            return obj
