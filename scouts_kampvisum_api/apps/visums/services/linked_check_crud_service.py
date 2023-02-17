from typing import List

from django.db import transaction
from django.utils import timezone

from apps.camps.models import CampType

from apps.visums.models import (
    LinkedSubCategory,
    SubCategory,
    Check,
    LinkedCheck,
)
from apps.visums.models.enums import CheckState


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedCheckCRUDService:
    @transaction.atomic
    def create_linked_checks(
        self, request, linked_sub_category: LinkedSubCategory, sub_category: SubCategory
    ) -> LinkedSubCategory:
        checks: List[Check] = Check.objects.safe_get(
            sub_category=sub_category,
            camp_types=linked_sub_category.category.category_set.visum.camp_types.all(),
            raise_error=True,
        )

        # logger.debug(
        #     "Linking %d checks to linked sub-category %s (%s)",
        #     len(checks),
        #     linked_sub_category.parent.name,
        #     linked_sub_category.id,
        # )

        for check in checks:
            self.create_linked_check(
                request=request,
                linked_sub_category=linked_sub_category,
                check=check,
            )

        return linked_sub_category

    @transaction.atomic
    def create_linked_check(
        self, request, linked_sub_category: LinkedSubCategory, check: Check
    ) -> LinkedCheck:
        linked_check: LinkedCheck = LinkedCheck.get_concrete_check_type(check)

        # logger.debug(
        #     "Creating LinkedCheck: %s (type: %s)",
        #     check.name,
        #     type(linked_check).__name__,
        # )

        linked_check.parent = check
        linked_check.sub_category = linked_sub_category
        linked_check.created_by = request.user

        if not check.check_type.should_be_checked():
            linked_check.check_state = CheckState.NOT_APPLICABLE
        elif check.is_required_for_validation:
            linked_check.check_state = CheckState.UNCHECKED
        else:
            linked_check.check_state = CheckState.NOT_APPLICABLE

        linked_check.full_clean()
        linked_check.save()

        return linked_check

    @ transaction.atomic
    def update_linked_checks(
        self,
        request,
        linked_sub_category: LinkedSubCategory,
        sub_category: SubCategory,
        current_camp_types: List[CampType] = None,
    ) -> LinkedSubCategory:
        camp_types: List[
            CampType
        ] = linked_sub_category.category.category_set.visum.camp_types.all()
        checks: List[Check] = Check.objects.safe_get(
            sub_category=sub_category,
            camp_types=camp_types,
            raise_error=True,
        )
        logger.debug(
            "Found %d Check instance(s) for camp_year %d and camp_types %s that should be linked to visum %s (%s)",
            len(checks),
            linked_sub_category.category.category_set.visum.year.year,
            ",".join(camp_type.camp_type for camp_type in camp_types),
            linked_sub_category.category.category_set.visum.name,
            linked_sub_category.category.category_set.visum.id,
        )

        current_linked_checks: List[LinkedCheck] = linked_sub_category.checks.all(
        )
        current_checks: List[Check] = [
            check.parent for check in current_linked_checks]
        logger.debug(
            "Found %d Check instance(s) for camp_year %d and camp_types %s that are currently linked to visum %s (%s)",
            len(current_checks),
            linked_sub_category.category.category_set.visum.year.year,
            ",".join(camp_type.camp_type for camp_type in camp_types),
            linked_sub_category.category.category_set.visum.name,
            linked_sub_category.category.category_set.visum.id,
        )

        # A check can be added, updated or removed from the visum or fixture
        for check in checks:
            linked_check: LinkedCheck = LinkedCheck.objects.safe_get(
                sub_category=linked_sub_category, parent=check
            )

            # Added Check
            if not linked_check:
                linked_check: LinkedCheck = self.create_linked_check(
                    request=request,
                    linked_sub_category=linked_sub_category,
                    check=check,
                )
            # Updated or re-added Check
            else:
                if (
                    linked_check.is_archived
                    and len(
                        [
                            camp_type
                            for camp_type in linked_check.parent.camp_types.all()
                            if camp_type in camp_types
                        ]
                    )
                    > 0
                ):
                    self.undelete_linked_check(
                        request=request, instance=linked_check)
                else:
                    self.update_linked_check(
                        request=request,
                        instance=linked_check,
                        check=check,
                        current_camp_types=current_camp_types,
                    )

                for current_check in current_checks:
                    if current_check.id == check.id:
                        current_checks.remove(current_check)

        # Deleted Check
        logger.debug(
            "REMAINING CURRENT CHECKS: %d (%s)",
            len(current_checks),
            ",".join(current_check.name for current_check in current_checks),
        )
        for linked_check in current_linked_checks:
            if linked_check.parent in current_checks:
                self.delete_linked_check(
                    request=request, instance=linked_check)

        return linked_sub_category

    @ transaction.atomic
    def update_linked_check(
        self,
        request,
        instance: LinkedCheck,
        check: Check,
        current_camp_types: List[CampType] = None,
    ) -> LinkedCheck:
        logger.debug(
            "Updating LinkedCheck '%s' for visum '%s' (%s)",
            instance.parent.name,
            instance.sub_category.category.category_set.visum.name,
            instance.sub_category.category.category_set.visum.id,
        )

        if not check.check_type.should_be_checked():
            instance.check_state = CheckState.NOT_APPLICABLE
        elif check.is_required_for_validation:
            instance.check_state = CheckState.UNCHECKED
        else:
            instance.check_state = CheckState.NOT_APPLICABLE

        instance.full_clean()
        instance.save()

        return instance

    @ transaction.atomic
    def delete_linked_checks(
        self, request, linked_sub_category: LinkedSubCategory
    ) -> LinkedCheck:
        for linked_check in linked_sub_category.checks.all():
            self.delete_linked_check(request=request, instance=linked_check)

    @ transaction.atomic
    def delete_linked_check(self, request, instance: LinkedCheck) -> LinkedCheck:
        instance.is_archived = True
        instance.archived_by = request.user
        instance.archived_on = timezone.now()

        instance.full_clean()
        instance.save()

        return instance

    @ transaction.atomic
    def undelete_linked_checks(
        self, request, linked_sub_category: LinkedSubCategory
    ) -> LinkedCheck:
        for linked_check in linked_sub_category.checks.all():
            self.undelete_linked_check(request=request, instance=linked_check)

    @ transaction.atomic
    def undelete_linked_check(self, request, instance: LinkedCheck) -> LinkedCheck:
        instance.is_archived = False
        instance.updated_by = request.user
        instance.updated_on = timezone.now()

        instance.full_clean()
        instance.save()

        return instance
