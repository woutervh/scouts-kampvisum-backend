import logging
from typing import List

from django.core.exceptions import ValidationError
from rest_framework import serializers

from apps.participants.serializers import InuitsParticipantSerializer

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
from apps.visums.services import LinkedCheckService
from apps.visums.urls import LinkedCheckEndpointFactory

from scouts_auth.inuits.serializers import PersistedFileSerializer
from scouts_auth.inuits.serializers.fields import (
    DatetypeAwareDateSerializerField,
    OptionalCharSerializerField,
    RequiredCharSerializerField,
    OptionalIntegerSerializerField,
)


logger = logging.getLogger(__name__)


class LinkedCheckSerializer(serializers.ModelSerializer):

    parent = CheckSerializer()
    endpoint = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()
    # state = serializers.ChoiceField(
    #     choices=CheckState.choices, default=CheckState.UNCHECKED
    # )
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
        check = LinkedCheckService.get_value_type(obj)

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

        self._state = CheckState.CHECKED if check.is_checked() else CheckState.UNCHECKED

        return value

    def get_state(self, obj: LinkedCheck):
        return self._state

    def to_internal_value(self, data: dict) -> dict:
        id = data.get("id", None)
        if id and len(data.keys()) == 1:
            linked_check = LinkedCheck.objects.safe_get(id=id)
            if linked_check:
                check = LinkedCheckService.get_value_type(linked_check)
                if check:
                    return check

        return super().to_internal_value(data)


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
    value = LinkedLocationSerializer(many=True)

    class Meta:
        model = LinkedLocationCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedLocationCheck) -> List[dict]:
        return LinkedLocationSerializer(obj.value, many=True).data


class LinkedCampLocationCheckSerializer(LinkedCheckSerializer):
    value = LinkedLocationSerializer(many=True)

    class Meta:
        model = LinkedLocationCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedLocationCheck) -> List[dict]:
        return LinkedLocationCheckSerializer().get_value(obj)


class LinkedParticipantCheckSerializer(LinkedCheckSerializer):
    value = InuitsParticipantSerializer(many=True)

    class Meta:
        model = LinkedParticipantCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedParticipantCheck) -> List[dict]:
        return InuitsParticipantSerializer(obj.value, many=True).data


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
