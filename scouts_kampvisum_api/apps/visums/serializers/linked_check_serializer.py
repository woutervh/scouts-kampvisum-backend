from typing import List

from django.core.exceptions import ValidationError
from rest_framework import serializers

from apps.participants.models.enums import ParticipantType
from apps.participants.serializers import VisumParticipantSerializer

from apps.locations.serializers import LinkedLocationSerializer

from apps.visums.models import (
    LinkedCheck,
    LinkedSimpleCheck,
    LinkedDateCheck,
    LinkedDurationCheck,
    LinkedLocationCheck,
    LinkedParticipantCheck,
    LinkedFileUploadCheck,
    LinkedCommentCheck,
    LinkedNumberCheck,
)
from apps.visums.models.enums import CheckState
from apps.visums.serializers import CheckSerializer

from scouts_auth.groupadmin.models import ScoutsGroup
from scouts_auth.scouts.permissions import CustomPermissionHelper
from scouts_auth.inuits.serializers import PersistedFileSerializer
from scouts_auth.inuits.serializers.fields import (
    DatetypeAwareDateSerializerField,
    RequiredCharSerializerField,
    OptionalCharSerializerField,
    OptionalIntegerSerializerField,
)

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedCheckSerializer(serializers.ModelSerializer):

    parent = CheckSerializer()
    endpoint = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    _state = CheckState.UNCHECKED

    class Meta:
        model = LinkedCheck
        exclude = ["sub_category"]

    def get_endpoint(self, obj: LinkedCheck):
        return LinkedCheckEndpointFactory.get_endpoint(
            "{}/{}".format(obj.parent.check_type.endpoint_route, obj.id)
        )

    def get_value(self, obj: LinkedCheck):
        # logger.debug("Getting value for %s with id %s", type(obj).__name__, obj.id)
        check: LinkedCheck = obj.get_value_type()

        permission_granted = True if (
            not obj.parent.requires_permission
            or CustomPermissionHelper.has_required_permission(
                request=self.context['request'],
                group_admin_id=obj.sub_category.category.category_set.visum.group,
                permission=obj.parent.requires_permission
            )
        ) else False

        if check.parent.check_type.is_simple_check():
            value = LinkedSimpleCheckSerializer.get_value(
                check, permission_granted)
        elif check.parent.check_type.is_date_check():
            value = LinkedDateCheckSerializer.get_value(
                check, permission_granted)
        elif check.parent.check_type.is_duration_check():
            value = LinkedDurationCheckSerializer.get_value(
                check, permission_granted)
        elif check.parent.check_type.is_location_check():
            value = LinkedLocationCheckSerializer.get_value(
                check, permission_granted)
        elif check.parent.check_type.is_camp_location_check():
            value = LinkedCampLocationCheckSerializer.get_value(
                check, permission_granted)
        elif check.parent.check_type.is_participant_member_check():
            value = LinkedParticipantMemberCheckSerializer.get_value(
                check, permission_granted)
        elif check.parent.check_type.is_participant_cook_check():
            value = LinkedParticipantCookCheckSerializer.get_value(
                check, permission_granted)
        elif check.parent.check_type.is_participant_leader_check():
            value = LinkedParticipantLeaderCheckSerializer.get_value(
                check, permission_granted)
        elif check.parent.check_type.is_participant_responsible_check():
            value = LinkedParticipantResponsibleCheckSerializer.get_value(
                check, permission_granted)
        elif check.parent.check_type.is_participant_adult_check():
            value = LinkedParticipantAdultCheckSerializer.get_value(
                check, permission_granted)
        elif check.parent.check_type.is_participant_check():
            value = LinkedParticipantCheckSerializer.get_value(
                check, permission_granted)
        elif check.parent.check_type.is_file_upload_check():
            value = LinkedFileUploadCheckSerializer.get_value(
                check, permission_granted)
        elif check.parent.check_type.is_comment_check():
            value = LinkedCommentCheckSerializer.get_value(
                check, permission_granted)
        elif check.parent.check_type.is_number_check():
            value = LinkedNumberCheckSerializer.get_value(
                check, permission_granted)
        else:
            value = check.value

        self._state = (
            CheckState.CHECKED
            if (obj.check_state == CheckState.CHECKED or not check.is_required_for_validation())
            else CheckState.UNCHECKED
        )

        return value

    def get_state(self, obj: LinkedCheck):
        return self._state

    def to_internal_value(self, data: dict) -> dict:
        pk = data.get("id", None)
        if id and len(data.keys()) == 1:
            linked_check = LinkedCheck.objects.safe_get(id=pk)
            if linked_check:
                check = linked_check.get_value_type()
                if check:
                    return check

        return super().to_internal_value(data)

    def to_representation(self, obj: LinkedCheck) -> dict:
        if obj.is_archived:
            return None

        data = super().to_representation(obj)

        data["readable_name"] = obj.readable_name

        return data


class LinkedSimpleCheckSerializer(LinkedCheckSerializer):
    value = serializers.ChoiceField(
        choices=CheckState.choices, default=CheckState.UNCHECKED
    )

    class Meta:
        model = LinkedSimpleCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedSimpleCheck, permission_granted: bool = True) -> dict:
        return obj.value

    @staticmethod
    def count_values(obj: LinkedSimpleCheck) -> int:
        return 1


class LinkedDateCheckSerializer(LinkedCheckSerializer):
    class Meta:
        model = LinkedDateCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedDateCheck, permission_granted: bool = True) -> dict:
        return obj.value

    @staticmethod
    def count_values(obj: LinkedDateCheck) -> int:
        return 1


class LinkedDurationCheckSerializer(LinkedCheckSerializer):

    start_date = DatetypeAwareDateSerializerField(required=True)
    end_date = DatetypeAwareDateSerializerField(required=True)

    class Meta:
        model = LinkedDurationCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedDurationCheck, permission_granted: bool = True) -> dict:
        data = dict()

        data["start_date"] = obj.start_date
        data["end_date"] = obj.end_date

        return data

    @staticmethod
    def count_values(obj: LinkedDurationCheck) -> int:
        return 2

    def validate(self, obj: dict) -> dict:
        start_date = obj.get("start_date", None)
        end_date = obj.get("end_date", None)

        if not start_date or not end_date:
            raise ValidationError("Start date and end date are required")

        if start_date > end_date:
            raise ValidationError(
                "Start date ({}) must come after end date ({})".format(
                    start_date, end_date
                )
            )

        return obj


class LinkedLocationCheckSerializer(LinkedCheckSerializer):
    locations = LinkedLocationSerializer(many=True)

    class Meta:
        model = LinkedLocationCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedLocationCheck, permission_granted: bool = True) -> dict:
        data = dict()

        if obj.has_value():
            data["center_latitude"] = obj.center_latitude
            data["center_longitude"] = obj.center_longitude
            data["zoom"] = obj.zoom

            if permission_granted:
                data["locations"] = LinkedLocationSerializer(
                    obj.locations, many=True).data
                data["data_count"] = obj.locations.count()
            else:
                data["locations"] = []
        else:
            data["locations"] = []

        return data

    @staticmethod
    def count_values(obj: LinkedLocationCheck) -> int:
        return obj.locations.count() if obj.parent.is_multiple else 1


class LinkedCampLocationCheckSerializer(LinkedCheckSerializer):
    locations = LinkedLocationSerializer(many=True)

    class Meta:
        model = LinkedLocationCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedLocationCheck, permission_granted: bool = True) -> List[dict]:
        data = LinkedLocationCheckSerializer.get_value(obj, permission_granted)

        data["is_camp_location"] = True

        return data

    @staticmethod
    def count_values(obj: LinkedLocationCheck) -> int:
        return LinkedLocationCheckSerializer.count_values(obj)


class LinkedParticipantCheckSerializer(LinkedCheckSerializer):
    participant_check_type = serializers.ChoiceField(
        choices=ParticipantType.choices, default=ParticipantType.PARTICIPANT
    )
    participants = VisumParticipantSerializer(many=True)

    class Meta:
        model = LinkedParticipantCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedParticipantCheck, permission_granted: bool = True) -> List[dict]:
        data = {}

        if obj.has_value():
            data["participant_check_type"] = obj.participant_check_type

            if permission_granted:
                data["participants"] = VisumParticipantSerializer(
                    obj.participants.all(), many=True
                ).data
            else:
                data["participants"] = []

            data["data_count"] = LinkedParticipantCheckSerializer.count_values(
                obj)

        return data

    @staticmethod
    def count_values(obj: LinkedParticipantCheck) -> int:
        return obj.participants.count() if obj.parent.is_multiple else 1


class LinkedParticipantMemberCheckSerializer(LinkedCheckSerializer):

    participants = VisumParticipantSerializer(many=True)

    class Meta:
        model = LinkedParticipantCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedParticipantCheck, permission_granted: bool = True) -> List[dict]:
        data = LinkedParticipantCheckSerializer.get_value(
            obj, permission_granted)

        data["participant_check_type"] = ParticipantType.MEMBER

        return data

    @staticmethod
    def count_values(obj: LinkedParticipantCheck) -> int:
        return LinkedParticipantCheckSerializer.count_values(obj)


class LinkedParticipantCookCheckSerializer(LinkedCheckSerializer):

    participants = VisumParticipantSerializer(many=True)

    class Meta:
        model = LinkedParticipantCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedParticipantCheck, permission_granted: bool = True) -> List[dict]:
        data = LinkedParticipantCheckSerializer.get_value(
            obj, permission_granted)

        data["participant_check_type"] = ParticipantType.COOK

        return data

    @staticmethod
    def count_values(obj: LinkedParticipantCheck) -> int:
        return LinkedParticipantCheckSerializer.count_values(obj)


class LinkedParticipantLeaderCheckSerializer(LinkedCheckSerializer):

    participants = VisumParticipantSerializer(many=True)

    class Meta:
        model = LinkedParticipantCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedParticipantCheck, permission_granted: bool = True) -> List[dict]:
        data = LinkedParticipantCheckSerializer.get_value(
            obj, permission_granted)

        data["participant_check_type"] = ParticipantType.LEADER

        return data

    @staticmethod
    def count_values(obj: LinkedParticipantCheck) -> int:
        return LinkedParticipantCheckSerializer.count_values(obj)


class LinkedParticipantResponsibleCheckSerializer(LinkedCheckSerializer):

    participants = VisumParticipantSerializer(many=True)

    class Meta:
        model = LinkedParticipantCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedParticipantCheck, permission_granted: bool = True) -> List[dict]:
        data = LinkedParticipantCheckSerializer.get_value(
            obj, permission_granted)

        data["participant_check_type"] = ParticipantType.RESPONSIBLE

        return data

    @staticmethod
    def count_values(obj: LinkedParticipantCheck) -> int:
        return LinkedParticipantCheckSerializer.count_values(obj)


class LinkedParticipantAdultCheckSerializer(LinkedCheckSerializer):

    participants = VisumParticipantSerializer(many=True)

    class Meta:
        model = LinkedParticipantCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedParticipantCheck, permission_granted: bool = True) -> List[dict]:
        data = LinkedParticipantCheckSerializer.get_value(
            obj, permission_granted)

        data["participant_check_type"] = ParticipantType.ADULT

        return data

    @staticmethod
    def count_values(obj: LinkedParticipantCheck) -> int:
        return LinkedParticipantCheckSerializer.count_values(obj)


class LinkedFileUploadCheckSerializer(LinkedCheckSerializer):
    value = PersistedFileSerializer(many=True)

    class Meta:
        model = LinkedFileUploadCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedFileUploadCheck, permission_granted: bool = True) -> list:
        return PersistedFileSerializer(obj.value.all(), many=True).data

    @staticmethod
    def count_values(obj: LinkedFileUploadCheck) -> int:
        return 1


class LinkedCommentCheckSerializer(LinkedCheckSerializer):
    value = OptionalCharSerializerField()

    class Meta:
        model = LinkedCommentCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedCommentCheck, permission_granted: bool = True) -> dict:
        # logger.debug("hm %s", str(obj))
        return obj.value

    @staticmethod
    def count_values(obj: LinkedCommentCheck) -> int:
        return 1


class LinkedNumberCheckSerializer(LinkedCheckSerializer):
    value = OptionalIntegerSerializerField()

    class Meta:
        model = LinkedNumberCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedNumberCheck, permission_granted: bool = True) -> dict:
        # logger.debug("hm %s", str(obj))
        return obj.value

    @staticmethod
    def count_values(obj: LinkedNumberCheck) -> int:
        return 1
