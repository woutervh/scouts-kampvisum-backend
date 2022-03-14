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
from apps.visums.urls import LinkedCheckEndpointFactory

from scouts_auth.inuits.serializers import PersistedFileSerializer
from scouts_auth.inuits.serializers.fields import (
    DatetypeAwareDateSerializerField,
    RequiredCharSerializerField,
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

        if check.parent.check_type.is_simple_check():
            value = LinkedSimpleCheckSerializer.get_value(check)
        elif check.parent.check_type.is_date_check():
            value = LinkedDateCheckSerializer.get_value(check)
        elif check.parent.check_type.is_duration_check():
            value = LinkedDurationCheckSerializer.get_value(check)
        elif check.parent.check_type.is_location_check():
            value = LinkedLocationCheckSerializer.get_value(check)
        elif check.parent.check_type.is_camp_location_check():
            value = LinkedCampLocationCheckSerializer.get_value(check)
        elif check.parent.check_type.is_participant_member_check():
            value = LinkedParticipantMemberCheckSerializer.get_value(check)
        elif check.parent.check_type.is_participant_cook_check():
            value = LinkedParticipantCookCheckSerializer.get_value(check)
        elif check.parent.check_type.is_participant_leader_check():
            value = LinkedParticipantLeaderCheckSerializer.get_value(check)
        elif check.parent.check_type.is_participant_responsible_check():
            value = LinkedParticipantResponsibleCheckSerializer.get_value(check)
        elif check.parent.check_type.is_participant_adult_check():
            value = LinkedParticipantAdultCheckSerializer.get_value(check)
        elif check.parent.check_type.is_participant_check():
            value = LinkedParticipantCheckSerializer.get_value(check)
        elif check.parent.check_type.is_file_upload_check():
            value = LinkedFileUploadCheckSerializer.get_value(check)
        elif check.parent.check_type.is_comment_check():
            value = LinkedCommentCheckSerializer.get_value(check)
        elif check.parent.check_type.is_number_check():
            value = LinkedNumberCheckSerializer.get_value(check)
        else:
            value = check.value

        self._state = (
            CheckState.CHECKED
            if check.is_checked() or not check.is_required_for_validation()
            else CheckState.UNCHECKED
        )

        return value

    def get_state(self, obj: LinkedCheck):
        return self._state

    def to_internal_value(self, data: dict) -> dict:
        id = data.get("id", None)
        if id and len(data.keys()) == 1:
            linked_check = LinkedCheck.objects.safe_get(id=id)
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
    def get_value(obj: LinkedSimpleCheck) -> dict:
        return obj.value


class LinkedDateCheckSerializer(LinkedCheckSerializer):
    class Meta:
        model = LinkedDateCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedDateCheck) -> dict:
        return obj.value


class LinkedDurationCheckSerializer(LinkedCheckSerializer):

    start_date = DatetypeAwareDateSerializerField(required=True)
    end_date = DatetypeAwareDateSerializerField(required=True)

    class Meta:
        model = LinkedDurationCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedDurationCheck) -> dict:
        data = dict()

        data["start_date"] = obj.start_date
        data["end_date"] = obj.end_date

        return data

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
    def get_value(obj: LinkedLocationCheck) -> List[dict]:
        data = dict()

        # data["is_camp_location"] = False
        data["center_latitude"] = obj.center_latitude
        data["center_longitude"] = obj.center_longitude
        data["zoom"] = obj.zoom
        data["locations"] = LinkedLocationSerializer(obj.locations, many=True).data

        return data


class LinkedCampLocationCheckSerializer(LinkedCheckSerializer):
    locations = LinkedLocationSerializer(many=True)

    class Meta:
        model = LinkedLocationCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedLocationCheck) -> List[dict]:
        data = LinkedLocationCheckSerializer().get_value(obj)

        data["is_camp_location"] = True

        return data


class LinkedParticipantCheckSerializer(LinkedCheckSerializer):
    participant_check_type = serializers.ChoiceField(
        choices=ParticipantType.choices, default=ParticipantType.PARTICIPANT
    )
    participants = VisumParticipantSerializer(many=True)

    class Meta:
        model = LinkedParticipantCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedParticipantCheck) -> List[dict]:
        data = {}

        data["participant_check_type"] = obj.participant_check_type
        data["participants"] = VisumParticipantSerializer(
            obj.participants.all(), many=True
        ).data

        return data


class LinkedParticipantMemberCheckSerializer(LinkedCheckSerializer):

    participants = VisumParticipantSerializer(many=True)

    class Meta:
        model = LinkedParticipantCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedParticipantCheck) -> List[dict]:
        data = LinkedParticipantCheckSerializer().get_value(obj)

        data["participant_check_type"] = ParticipantType.MEMBER

        return data


class LinkedParticipantCookCheckSerializer(LinkedCheckSerializer):

    participants = VisumParticipantSerializer(many=True)

    class Meta:
        model = LinkedParticipantCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedParticipantCheck) -> List[dict]:
        data = LinkedParticipantCheckSerializer().get_value(obj)

        data["participant_check_type"] = ParticipantType.COOK

        return data


class LinkedParticipantLeaderCheckSerializer(LinkedCheckSerializer):

    participants = VisumParticipantSerializer(many=True)

    class Meta:
        model = LinkedParticipantCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedParticipantCheck) -> List[dict]:
        data = LinkedParticipantCheckSerializer().get_value(obj)

        data["participant_check_type"] = ParticipantType.LEADER

        return data


class LinkedParticipantResponsibleCheckSerializer(LinkedCheckSerializer):

    participants = VisumParticipantSerializer(many=True)

    class Meta:
        model = LinkedParticipantCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedParticipantCheck) -> List[dict]:
        data = LinkedParticipantCheckSerializer().get_value(obj)

        data["participant_check_type"] = ParticipantType.RESPONSIBLE

        return data


class LinkedParticipantAdultCheckSerializer(LinkedCheckSerializer):

    participants = VisumParticipantSerializer(many=True)

    class Meta:
        model = LinkedParticipantCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedParticipantCheck) -> List[dict]:
        data = LinkedParticipantCheckSerializer().get_value(obj)

        data["participant_check_type"] = ParticipantType.ADULT

        return data


class LinkedFileUploadCheckSerializer(LinkedCheckSerializer):
    value = PersistedFileSerializer(many=True)

    class Meta:
        model = LinkedFileUploadCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedFileUploadCheck) -> list:
        return PersistedFileSerializer(obj.value.all(), many=True).data


class LinkedCommentCheckSerializer(LinkedCheckSerializer):
    value = RequiredCharSerializerField()

    class Meta:
        model = LinkedCommentCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedCommentCheck) -> dict:
        # logger.debug("hm %s", str(obj))
        return obj.value


class LinkedNumberCheckSerializer(LinkedCheckSerializer):
    value = OptionalIntegerSerializerField()

    class Meta:
        model = LinkedNumberCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedNumberCheck) -> dict:
        # logger.debug("hm %s", str(obj))
        return obj.value
