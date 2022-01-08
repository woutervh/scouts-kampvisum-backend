import logging

from rest_framework import serializers

from apps.visums.models import (
    LinkedCheck,
    LinkedSimpleCheck,
    LinkedDateCheck,
    LinkedDurationCheck,
    LinkedLocationCheck,
    LinkedLocationContactCheck,
    LinkedMemberCheck,
    LinkedFileUploadCheck,
    LinkedCommentCheck,
)
from apps.visums.models.enums import CheckState
from apps.visums.serializers import VisumCheckSerializer
from apps.visums.services import LinkedCheckService
from apps.visums.urls import LinkedCheckEndpointFactory


logger = logging.getLogger(__name__)


class LinkedCheckSerializer(serializers.ModelSerializer):

    parent = VisumCheckSerializer()
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
        elif check.parent.check_type.is_duration_check():
            value = "({},{})".format(check.start_date, check.end_date)
        else:
            value = check.value

        logger.debug(
            "%s value: %s (%s)",
            type(check).__name__,
            value,
            type(value).__name__,
        )

        return value

    def get_simple_check_value(self, obj: LinkedCheck, check: LinkedSimpleCheck):
        logger.debug("CHECK VALUE: %s", check.value)

        return check.value


class LinkedSimpleCheckSerializer(LinkedCheckSerializer):

    value = serializers.ChoiceField(
        choices=CheckState.choices, default=CheckState.UNCHECKED
    )

    class Meta:
        model = LinkedSimpleCheck
        fields = "__all__"


class LinkedDateCheckSerializer(LinkedCheckSerializer):
    class Meta:
        model = LinkedDateCheck
        fields = "__all__"


class LinkedDurationCheckSerializer(LinkedCheckSerializer):
    class Meta:
        model = LinkedDurationCheck
        fields = ["start_date", "end_date"]


class LinkedLocationCheckSerializer(LinkedCheckSerializer):
    class Meta:
        model = LinkedLocationCheck
        fields = "__all__"


class LinkedLocationContactCheckSerializer(LinkedCheckSerializer):
    class Meta:
        model = LinkedLocationContactCheck
        fields = "__all__"


class LinkedMemberCheckSerializer(LinkedCheckSerializer):
    class Meta:
        model = LinkedMemberCheck
        fields = "__all__"


class LinkedFileUploadCheckSerializer(LinkedCheckSerializer):
    class Meta:
        model = LinkedFileUploadCheck
        fields = "__all__"


class LinkedCommentCheckSerializer(LinkedCheckSerializer):
    class Meta:
        model = LinkedCommentCheck
        fields = "__all__"
