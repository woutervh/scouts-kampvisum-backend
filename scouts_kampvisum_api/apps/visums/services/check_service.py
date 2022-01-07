import logging

from django.core.exceptions import ValidationError

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
    VisumCheck,
    CheckType,
)


logger = logging.getLogger(__name__)


class CheckService:
    def link_checks(
        self, request, linked_sub_category: LinkedSubCategory, sub_category: SubCategory
    ) -> LinkedSubCategory:
        logger.debug("Linking checks")

        for check in sub_category.checks.all():
            linked_check = self._get_specific_check_type(request, check)
            logger.debug(
                "Linked check: %s (type: %s)", check.name, type(linked_check).__name__
            )

            linked_check.parent = check
            linked_check.sub_category = linked_sub_category

            linked_check.full_clean()
            linked_check.save()

        return linked_sub_category

    def _get_specific_check_type(self, request, check: VisumCheck):
        check_type: CheckType = check.check_type

        if check_type.is_simple_check():
            return LinkedSimpleCheck()
        elif check_type.is_date_check():
            return LinkedDateCheck()
        elif check_type.is_duration_check():
            return LinkedDurationCheck()
        elif check_type.is_location_check():
            return LinkedLocationCheck()
        elif check_type.is_location_contact_check():
            return LinkedLocationContactCheck()
        elif check_type.is_member_check():
            return LinkedMemberCheck()
        elif check_type.is_contact_check():
            return LinkedContactCheck()
        elif check_type.is_file_upload_check():
            LinkedFileUploadCheck()
        elif check_type.is_input_check():
            return LinkedInputCheck()
        elif check_type.is_information_check():
            return LinkedInformationCheck()
        else:
            raise ValidationError(
                "Check type {} is not recognized".format(check_type.check_type)
            )
