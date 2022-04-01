from typing import List

from django.db import transaction
from django.utils import timezone

from apps.camps.models import CampType

from apps.visums.models import LinkedCategory, Category, LinkedSubCategory, SubCategory
from apps.visums.services import LinkedCheckCRUDService


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedSubCategoryService:

    linked_check_service = LinkedCheckCRUDService()

    @transaction.atomic
    def create_linked_sub_categories(
        self, request, linked_category: LinkedCategory, category: Category
    ) -> LinkedCategory:
        sub_categories: List[SubCategory] = SubCategory.objects.safe_get(
            category=category,
            camp_types=linked_category.category_set.visum.camp_types.all(),
            raise_error=True,
        )

        logger.debug(
            "Linking %d sub-categories to category %s (%s)",
            len(sub_categories),
            linked_category.id,
            linked_category.parent.name,
        )

        for sub_category in sub_categories:
            self.create_linked_sub_category(
                request=request,
                linked_category=linked_category,
                sub_category=sub_category,
            )

        return linked_category

    @transaction.atomic
    def create_linked_sub_category(
        self, request, linked_category: LinkedCategory, sub_category: SubCategory
    ) -> LinkedSubCategory:
        logger.debug("Creating LinkedSubCategory '%s'", sub_category.name)

        linked_sub_category = LinkedSubCategory()

        linked_sub_category.parent = sub_category
        linked_sub_category.category = linked_category

        linked_sub_category.full_clean()
        linked_sub_category.save()

        self.linked_check_service.create_linked_checks(
            request,
            linked_sub_category=linked_sub_category,
            sub_category=sub_category,
        )

        return linked_sub_category

    @transaction.atomic
    def update_linked_sub_categories(
        self,
        request,
        linked_category: LinkedCategory,
        category: Category,
        current_camp_types: List[CampType] = None,
    ) -> LinkedCategory:
        camp_types: List[CampType] = linked_category.category_set.visum.camp_types.all()
        sub_categories: List[SubCategory] = SubCategory.objects.safe_get(
            category=category,
            camp_types=camp_types,
        )
        logger.debug(
            "Found %d SubCategory instance(s) for camp_year %d and camp_types %s that should be linked to visum %s (%s)",
            len(sub_categories),
            linked_category.category_set.visum.camp.year.year,
            ",".join(camp_type.camp_type for camp_type in camp_types),
            linked_category.category_set.visum.camp.name,
            linked_category.category_set.visum.camp.name,
        )

        current_linked_sub_categories: List[
            LinkedSubCategory
        ] = linked_category.sub_categories.all()
        current_sub_categories: List[SubCategory] = [
            sub_category.parent for sub_category in current_linked_sub_categories
        ]
        logger.debug(
            "Found %d SubCategory instance(s) for camp_year %d and camp_types %s that are currently linked to visum %s (%s)",
            len(current_sub_categories),
            linked_category.category_set.visum.camp.year.year,
            ",".join(camp_type.camp_type for camp_type in camp_types),
            linked_category.category_set.visum.camp.name,
            linked_category.category_set.visum.id,
        )

        # A sub-category can be added, updated or removed from the visum or fixture
        for sub_category in sub_categories:
            linked_sub_category: LinkedSubCategory = LinkedSubCategory.objects.safe_get(
                category=linked_category, parent=sub_category
            )

            # Added SubCategory
            if not linked_sub_category:
                linked_sub_category: LinkedSubCategory = (
                    self.create_linked_sub_category(
                        request=request,
                        linked_category=linked_category,
                        sub_category=sub_category,
                    )
                )
            # Updated or re-added SubCategory
            else:
                if (
                    linked_sub_category.is_archived
                    and len(
                        [
                            camp_type
                            for camp_type in linked_sub_category.parent.camp_types.all()
                            if camp_type in camp_types
                        ]
                    )
                    > 0
                ):
                    self.undelete_linked_sub_category(
                        request=request, instance=linked_sub_category
                    )
                else:
                    self.update_linked_sub_category(
                        request=request,
                        instance=linked_sub_category,
                        sub_category=sub_category,
                        current_camp_types=current_camp_types,
                    )

                for current_sub_category in current_sub_categories:
                    if current_sub_category.id == sub_category.id:
                        current_sub_categories.remove(current_sub_category)

        # Deleted SubCategory
        logger.debug(
            "REMAINING CURRENT SUB-CATEGORIES: %d (%s)",
            len(current_sub_categories),
            ",".join(
                current_sub_category.name
                for current_sub_category in current_sub_categories
            ),
        )
        for linked_sub_category in current_linked_sub_categories:
            if linked_sub_category.parent in current_sub_categories:
                self.delete_linked_sub_category(
                    request=request, instance=linked_sub_category
                )

        return linked_category

    @transaction.atomic
    def update_linked_sub_category(
        self,
        request,
        instance: LinkedSubCategory,
        sub_category: SubCategory,
        current_camp_types: List[CampType] = None,
    ) -> LinkedSubCategory:
        logger.debug(
            "Updating LinkedSubCategory '%s' for visum '%s' (%s)",
            instance.parent.name,
            instance.category.category_set.visum.camp.name,
            instance.category.category_set.visum.id,
        )
        self.linked_check_service.update_linked_checks(
            request,
            linked_sub_category=instance,
            sub_category=sub_category,
            current_camp_types=current_camp_types,
        )

        return instance

    @transaction.atomic
    def delete_linked_sub_categories(
        self, request, linked_category: LinkedCategory
    ) -> LinkedSubCategory:
        for linked_sub_category in linked_category.sub_categories.all():
            self.delete_linked_sub_category(
                request=request, instance=linked_sub_category
            )

    @transaction.atomic
    def delete_linked_sub_category(
        self, request, instance: LinkedSubCategory
    ) -> LinkedSubCategory:
        instance.is_archived = True
        instance.archived_by = request.user
        instance.archived_on = timezone.now()

        instance.full_clean()
        instance.save()

        self.linked_check_service.delete_linked_checks(
            request=request, linked_sub_category=instance
        )

        return instance

    @transaction.atomic
    def undelete_linked_sub_categories(
        self, request, linked_category: LinkedCategory
    ) -> LinkedSubCategory:
        for linked_sub_category in linked_category.sub_categories.all():
            self.undelete_linked_sub_category(
                request=request, instance=linked_sub_category
            )

    @transaction.atomic
    def undelete_linked_sub_category(
        self, request, instance: LinkedSubCategory
    ) -> LinkedSubCategory:
        instance.is_archived = False
        instance.updated_by = request.user
        instance.updated_on = timezone.now()

        instance.full_clean()
        instance.save()

        self.linked_check_service.undelete_linked_checks(
            request=request, linked_sub_category=instance
        )

        return instance
