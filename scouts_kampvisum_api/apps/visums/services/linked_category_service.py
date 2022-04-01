from typing import List

from django.db import transaction
from django.utils import timezone

from apps.camps.models import CampType

from apps.visums.models import LinkedCategorySet, LinkedCategory, Category
from apps.visums.services import LinkedSubCategoryService


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedCategoryService:

    linked_sub_category_service = LinkedSubCategoryService()

    @transaction.atomic
    def create_linked_categories(
        self,
        request,
        linked_category_set: LinkedCategorySet,
    ) -> LinkedCategorySet:
        categories: List[Category] = Category.objects.safe_get(
            camp_year=linked_category_set.visum.camp.year,
            camp_types=linked_category_set.visum.camp_types.all(),
            raise_error=True,
        )
        logger.debug(
            "Linking %d Category instances for camp_year %d and camp_types %s to visum %s",
            len(categories),
            linked_category_set.visum.camp.year.year,
            ",".join(
                camp_type.camp_type
                for camp_type in linked_category_set.visum.camp_types.all()
            ),
            linked_category_set.visum.camp.name,
        )

        for category in categories:
            self.create_linked_category(
                request=request,
                linked_category_set=linked_category_set,
                category=category,
            )

        return linked_category_set

    @transaction.atomic
    def create_linked_category(
        self, request, linked_category_set: LinkedCategorySet, category: Category
    ) -> LinkedCategory:
        logger.debug(
            "Creating LinkedCategory '%s' for visum '%s' (%s)",
            category.name,
            linked_category_set.visum.camp.name,
            linked_category_set.visum.id,
        )

        linked_category = LinkedCategory()

        linked_category.parent = category
        linked_category.category_set = linked_category_set

        linked_category.full_clean()
        linked_category.save()

        self.linked_sub_category_service.create_linked_sub_categories(
            request, linked_category=linked_category, category=category
        )

        return linked_category

    @transaction.atomic
    def update_linked_categories(
        self,
        request,
        linked_category_set: LinkedCategorySet,
        current_camp_types: List[CampType] = None,
    ) -> LinkedCategorySet:
        camp_types: List[CampType] = linked_category_set.visum.camp_types.all()
        categories: List[Category] = Category.objects.safe_get(
            camp_year=linked_category_set.visum.camp.year,
            camp_types=camp_types,
            raise_error=True,
        )
        logger.debug(
            "Found %d Category instance(s) for camp_year %d and camp_types %s that should be linked to visum %s (%s)",
            len(categories),
            linked_category_set.visum.camp.year.year,
            ",".join(camp_type.camp_type for camp_type in camp_types),
            linked_category_set.visum.camp.name,
            linked_category_set.visum.camp.name,
        )

        current_linked_categories: List[
            LinkedCategory
        ] = linked_category_set.categories.all()
        current_categories: List[Category] = [
            category.parent for category in current_linked_categories
        ]
        logger.debug(
            "Found %d Category instance(s) for camp_year %d and camp_types %s that are currently linked to visum %s (%s)",
            len(current_categories),
            linked_category_set.visum.camp.year.year,
            ",".join(camp_type.camp_type for camp_type in camp_types),
            linked_category_set.visum.camp.name,
            linked_category_set.visum.id,
        )

        # A category can be added, updated or removed from the visum or fixture
        for category in categories:
            linked_category: LinkedCategory = LinkedCategory.objects.safe_get(
                category_set=linked_category_set, parent=category
            )

            # Added Category
            if not linked_category:
                linked_category: LinkedCategory = self.create_linked_category(
                    request=request,
                    linked_category_set=linked_category_set,
                    category=category,
                )
            # Updated or re-added Category
            else:
                if (
                    linked_category.is_archived
                    and len(
                        [
                            camp_type
                            for camp_type in linked_category.parent.camp_types.all()
                            if camp_type in camp_types
                        ]
                    )
                    > 0
                ):
                    self.undelete_linked_category(
                        request=request, instance=linked_category
                    )
                else:
                    self.update_linked_category(
                        request=request,
                        instance=linked_category,
                        category=category,
                        current_camp_types=current_camp_types,
                    )

                for current_category in current_categories:
                    if current_category.id == category.id:
                        current_categories.remove(current_category)

        # Deleted Category
        logger.debug(
            "REMAINING CURRENT CATEGORIES: %d (%s)",
            len(current_categories),
            ", ".join(current_category.name for current_category in current_categories),
        )
        for linked_category in current_linked_categories:
            if linked_category.parent in current_categories:
                self.delete_linked_category(request=request, instance=linked_category)

        return linked_category_set

    @transaction.atomic
    def update_linked_category(
        self,
        request,
        instance: LinkedCategory,
        category: Category,
        current_camp_types: List[CampType] = None,
    ) -> LinkedCategory:
        logger.debug(
            "Updating LinkedCategory '%s' for visum '%s' (%s)",
            instance.parent.name,
            instance.category_set.visum.camp.name,
            instance.category_set.visum.id,
        )

        self.linked_sub_category_service.update_linked_sub_categories(
            request,
            linked_category=instance,
            category=category,
            current_camp_types=current_camp_types,
        )

        return instance

    @transaction.atomic
    def delete_linked_category(
        self, request, instance: LinkedCategory
    ) -> LinkedCategory:
        instance.is_archived = True
        instance.archived_by = request.user
        instance.archived_on = timezone.now()

        instance.full_clean()
        instance.save()

        self.linked_sub_category_service.delete_linked_sub_categories(
            request=request, linked_category=instance
        )

        return instance

    @transaction.atomic
    def undelete_linked_category(
        self, request, instance: LinkedCategory
    ) -> LinkedCategory:
        instance.is_archived = False
        instance.updated_by = request.user
        instance.updated_on = timezone.now()

        instance.full_clean()
        instance.save()

        self.linked_sub_category_service.undelete_linked_sub_categories(
            request=request, linked_category=instance
        )

        return instance
