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
    LinkedFileUploadCheck,
    LinkedCommentCheck,
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
            logger.error("LinkedSimpleCheck with id %s not found", check_id)
            raise Http404

    def update_simple_check(self, instance: LinkedSimpleCheck, **data):
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )
        instance.value = data.get("value", None)

        instance.full_clean()
        instance.save()

        return instance

    def get_date_check(self, check_id):
        try:
            return LinkedDateCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedDateCheck.DoesNotExist:
            raise Http404

    def get_duration_check(self, check_id):
        try:
            return LinkedDurationCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedDurationCheck.DoesNotExist:
            logger.error("LinkedDurationCheck with id %s not found", check_id)
            raise Http404

    def update_duration_check(self, instance: LinkedDurationCheck, **data):
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )
        instance.start_date = data.get("start_date", None)
        instance.end_date = data.get("end_date", None)

        instance.full_clean()
        instance.save()

        return instance

    def get_location_check(self, check_id):
        try:
            return LinkedLocationCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedLocationCheck.DoesNotExist:
            logger.error("LinkedLocationCheck with id %s not found", check_id)
            raise Http404

    def get_location_contact_check(self, check_id):
        try:
            return LinkedLocationContactCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedLocationContactCheck.DoesNotExist:
            logger.error("LinkedLocationContactCheck with id %s not found", check_id)
            raise Http404

    def get_member_check(self, check_id):
        try:
            return LinkedMemberCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedMemberCheck.DoesNotExist:
            logger.error("LinkedMemberCheck with id %s not found", check_id)
            raise Http404

    def get_file_upload_check(self, check_id):
        try:
            return LinkedFileUploadCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedFileUploadCheck.DoesNotExist:
            logger.error("LinkedFileUploadCheck with id %s not found", check_id)
            raise Http404

    def get_comment_check(self, check_id):
        try:
            return LinkedCommentCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedCommentCheck.DoesNotExist:
            logger.error("LinkedCommentCheck with id %s not found", check_id)
            raise Http404

    def update_comment_check(self, instance: LinkedCommentCheck, **data):
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )
        instance.value = data.get("value", None)

        instance.full_clean()
        instance.save()

        return instance
