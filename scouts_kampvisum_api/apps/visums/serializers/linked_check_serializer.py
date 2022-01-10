import logging

from rest_framework import serializers

from apps.locations.serializers import CampLocationSerializer
from apps.visums.models import (
    LinkedCheck,
    LinkedSimpleCheck,
    LinkedDateCheck,
    LinkedDurationCheck,
    LinkedLocationCheck,
    LinkedMemberCheck,
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
    RequiredCharSerializerField,
)


logger = logging.getLogger(__name__)


class LinkedCheckSerializer(serializers.ModelSerializer):

    parent = CheckSerializer()
    endpoint = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    class Meta:
        model = LinkedCheck
        exclude = ["sub_category"]

    def get_endpoint(self, obj: LinkedCheck):
        return LinkedCheckEndpointFactory.get_endpoint(
            "{}/{}".format(obj.parent.check_type.endpoint_route, obj.id)
        )

    def get_value(self, obj: LinkedCheck):
        logger.debug("Getting value for %s with id %s", type(obj).__name__, obj.id)
        check = LinkedCheckService.get_value_type(obj)

        if check.parent.check_type.is_simple_check():
            value = self.get_simple_check_value(obj, check)
        elif check.parent.check_type.is_date_check():
            value = self.get_date_check_value(obj, check)
        elif check.parent.check_type.is_duration_check():
            value = self.get_duration_check_value(obj, check)
        elif check.parent.check_type.is_location_check():
            value = self.get_location_check_value(obj, check)
        elif check.parent.check_type.is_camp_location_check():
            value = self.get_camp_location_check_value(obj, check)
        elif check.parent.check_type.is_member_check():
            value = self.get_member_check_value(obj, check)
        elif check.parent.check_type.is_file_upload_check():
            value = self.get_file_upload_check_value(obj, check)
        elif check.parent.check_type.is_comment_check():
            value = self.get_comment_check_value(obj, check)

        else:
            value = check.value

        logger.debug(
            "%s value: %s (%s)",
            type(check).__name__,
            value,
            type(value).__name__,
        )

        return value

    def get_simple_check_value(
        self, obj: LinkedCheck, check: LinkedSimpleCheck
    ) -> CheckState:
        logger.debug("SIMPLE CHECK VALUE: %s", check.value)

        data = LinkedSimpleCheckSerializer().get_value(check)

        logger.debug("SIMPLE CHECK DATA: %s", data)

        return data

    def get_date_check_value(
        self, obj: LinkedCheck, check: LinkedDateCheck
    ) -> CheckState:
        logger.debug("DATA CHECK VALUE: %s", check.value)

        data = LinkedDateCheckSerializer().get_value(check)

        logger.debug("DATE CHECK DATA: %s", data)

        return data

    def get_duration_check_value(
        self, obj: LinkedCheck, check: LinkedDurationCheck
    ) -> dict:
        logger.debug("DURATION CHECK DATA: %s", str(check))

        data = LinkedDurationCheckSerializer().get_value(check)

        logger.debug("DURATION CHECK DATA: %s", data)

        return data

    def get_location_check_value(
        self, obj: LinkedCheck, check: LinkedLocationCheck
    ) -> dict:
        logger.debug("LOCATION CHECK DATA: %s", str(check))

        data = LinkedLocationCheckSerializer().get_value(check)

        logger.debug("LOCATION CHECK DATA: %s", data)

        return data

    def get_camp_location_check_value(
        self, obj: LinkedCheck, check: LinkedLocationCheck
    ) -> dict:
        logger.debug("CAMP LOCATION CHECK DATA: %s", str(check))

        data = LinkedCampLocationCheckSerializer().get_value(check)

        logger.debug("CAMP LOCATION CHECK DATA: %s", data)

        return data

    def get_member_check_value(
        self, obj: LinkedCheck, check: LinkedMemberCheck
    ) -> dict:
        logger.debug("MEMBER CHECK DATA: %s", str(check))

        data = LinkedMemberCheckSerializer().get_value(check)

        logger.debug("MEMBER CHECK DATA: %s", data)

        return data

    def get_file_upload_check_value(
        self, obj: LinkedCheck, check: LinkedFileUploadCheck
    ) -> dict:
        logger.debug("FILE UPLOAD CHECK DATA: %s", str(check))

        data = LinkedFileUploadCheckSerializer().get_value(check)

        logger.debug("FILE UPLOAD CHECK DATA: %s", data)

        return data

    def get_comment_check_value(
        self, obj: LinkedCheck, check: LinkedCommentCheck
    ) -> dict:
        logger.debug("COMMENT CHECK DATA: %s", str(check))

        data = LinkedCommentCheckSerializer().get_value(check)

        logger.debug("COMMENT CHECK DATA: %s", data)

        return data


class LinkedSimpleCheckSerializer(LinkedCheckSerializer):

    value = serializers.ChoiceField(
        choices=CheckState.choices, default=CheckState.UNCHECKED
    )

    class Meta:
        model = LinkedSimpleCheck
        fields = "__all__"

    def get_value(self, obj: LinkedSimpleCheck) -> dict:
        return obj.value


class LinkedDateCheckSerializer(LinkedCheckSerializer):
    class Meta:
        model = LinkedDateCheck
        fields = "__all__"

    def get_value(self, obj: LinkedDateCheck) -> dict:
        return obj.value


class LinkedDurationCheckSerializer(LinkedCheckSerializer):

    start_date = DatetypeAwareDateSerializerField(required=True)
    end_date = DatetypeAwareDateSerializerField(required=True)

    class Meta:
        model = LinkedDurationCheck
        fields = "__all__"

    def get_value(self, obj: LinkedDurationCheck) -> dict:
        data = dict()

        data["start_date"] = obj.start_date
        data["end_date"] = obj.end_date

        return data


class LinkedLocationCheckSerializer(LinkedCheckSerializer):

    locations = CampLocationSerializer(many=True)

    class Meta:
        model = LinkedLocationCheck
        fields = "__all__"

    def get_value(self, obj: LinkedLocationCheck) -> dict:
        return {}


class LinkedCampLocationCheckSerializer(LinkedCheckSerializer):

    locations = CampLocationSerializer(many=True)

    class Meta:
        model = LinkedLocationCheck
        fields = "__all__"

    def get_value(self, obj: LinkedLocationCheck) -> dict:
        data = LinkedLocationCheck().get_value(obj)

        data["is_camp_location"] = True

        return data


class LinkedMemberCheckSerializer(LinkedCheckSerializer):
    class Meta:
        model = LinkedMemberCheck
        fields = "__all__"

    def get_value(self, obj: LinkedMemberCheck) -> dict:
        return obj.value


class LinkedFileUploadCheckSerializer(LinkedCheckSerializer):
    file = PersistedFileSerializer()

    class Meta:
        model = LinkedFileUploadCheck
        fields = "__all__"

    def get_value(self, obj: LinkedFileUploadCheck) -> dict:
        return obj.value


class LinkedCommentCheckSerializer(LinkedCheckSerializer):
    value = RequiredCharSerializerField()

    class Meta:
        model = LinkedCommentCheck
        fields = "__all__"

    def get_value(self, obj: LinkedCommentCheck) -> dict:
        logger.debug("hm %s", str(obj))
        return obj.value
