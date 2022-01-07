import logging

from django.http import Http404

from apps.visums.models import (
    LinkedSubCategory,
    SubCategory,
    LinkedCheck,
    LinkedSimpleCheck,
    LinkedDateCheck,
    LinkedDurationCheck,
    LinkedLocationCheck,
    LinkedLocationContactCheck,
    LinkedMemberCheck,
    LinkedContactCheck,
    LinkedFileUploadCheck,
    LinkedInputCheck,
    LinkedInformationCheck,
)


logger = logging.getLogger(__name__)


class LinkedCheckService:
    @staticmethod
    def get_value_type(check: LinkedCheck):
        concrete_type = LinkedCheck.get_concrete_check_type(check.parent)

        check = concrete_type.__class__.objects.get(linkedcheck_ptr=check.id)
        # logger.debug("CONCRETE CHECK: %s", check)

        return check

    def get_simple_check(self, check_id):
        try:
            return LinkedSimpleCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedSimpleCheck.DoesNotExist:
            raise Http404

    def update_simple_check(self, instance: LinkedSimpleCheck, **data):
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )
        instance.value = data.get("value", None)

        instance.full_clean()
        instance.save()

        return instance

    def get_duration_check(self, check_id):
        try:
            return LinkedDurationCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedDurationCheck.DoesNotExist:
            raise Http404

    def get_date_check(self, check_id):
        try:
            return LinkedDateCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedDateCheck.DoesNotExist:
            raise Http404

    def get_location_check(self, check_id):
        try:
            return LinkedLocationCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedLocationCheck.DoesNotExist:
            raise Http404

    def get_location_contact_check(self, check_id):
        try:
            return LinkedLocationContactCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedLocationContactCheck.DoesNotExist:
            raise Http404

    def get_member_check(self, check_id):
        try:
            return LinkedMemberCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedMemberCheck.DoesNotExist:
            raise Http404

    def get_contact_check(self, check_id):
        try:
            return LinkedContactCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedContactCheck.DoesNotExist:
            raise Http404

    def get_file_upload_check(self, check_id):
        try:
            return LinkedFileUploadCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedFileUploadCheck.DoesNotExist:
            raise Http404

    def get_input_check(self, check_id):
        try:
            return LinkedInputCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedInputCheck.DoesNotExist:
            raise Http404

    def get_information_check(self, check_id):
        try:
            return LinkedInformationCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedInformationCheck.DoesNotExist:
            raise Http404
