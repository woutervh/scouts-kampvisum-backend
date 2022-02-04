import logging

from rest_framework import serializers

from apps.participants.serializers import InuitsParticipantSerializer
from apps.locations.serializers import CampLocationSerializer
from apps.visums.models import (
    LinkedCheck,
    LinkedSimpleCheck,
    LinkedDateCheck,
    LinkedDurationCheck,
    LinkedLocationCheck,
    LinkedParticipantCheck,
    LinkedFileUploadCheck,
    LinkedCommentCheck,
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

        else:
            value = check.value
        
        self._state = CheckState.CHECKED if check.is_checked() else CheckState.UNCHECKED

        return value

    def get_state(self, obj: LinkedCheck):
        return self._state
    
    # def to_representation(self, obj: LinkedCheck) -> dict:
    #     logger.debug("LINKED CHECK SERIALIZER TO_REPRESENTATION: %s", obj)
        
    #     data = super().to_representation(obj)
        
    #     logger.debug("LINKED CHECK SERIALIZER TO_REPRESENTATION: %s", data)

    #     data["state"] = obj.is_checked()
        
    #     return data

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


class LinkedLocationCheckSerializer(LinkedCheckSerializer):

    name = OptionalCharSerializerField()
    contact_name = OptionalCharSerializerField()
    contact_phone = OptionalCharSerializerField()
    contact_email = OptionalCharSerializerField()
    locations = CampLocationSerializer(many=True)

    class Meta:
        model = LinkedLocationCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedLocationCheck) -> dict:
        # logger.debug("LOCATION SERIALIZER DATA: %s", str(obj))
        data = dict()

        data["id"] = obj.id
        data["name"] = obj.name
        data["contact_name"] = obj.contact_name
        data["contact_phone"] = obj.contact_phone
        data["contact_email"] = obj.contact_email
        data["center_latitude"] = obj.center_latitude
        data["center_longitude"] = obj.center_longitude
        data["zoom"] = obj.zoom
        data["locations"] = CampLocationSerializer(obj.locations, many=True).data

        return data


class LinkedCampLocationCheckSerializer(LinkedCheckSerializer):
    locations = CampLocationSerializer(many=True)

    class Meta:
        model = LinkedLocationCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedLocationCheck) -> dict:
        data = LinkedLocationCheckSerializer().get_value(obj)

        data["locations"] = CampLocationSerializer(obj.locations, many=True).data
        data["is_camp_location"] = True

        return data


class LinkedParticipantCheckSerializer(LinkedCheckSerializer):
    value = InuitsParticipantSerializer(many=True)

    class Meta:
        model = LinkedParticipantCheck
        fields = "__all__"

    @staticmethod
    def get_value(obj: LinkedParticipantCheck) -> dict:
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
