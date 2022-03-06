from typing import List

from django.db import transaction

from apps.visums.models import LinkedCategory, Category, LinkedSubCategory, SubCategory
from apps.visums.services import CheckService


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class SubCategoryService:
    check_service = CheckService()

    @transaction.atomic
    def link_sub_categories(
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
            self.link_sub_category(
                request=request,
                linked_category=linked_category,
                sub_category=sub_category,
            )

        return linked_category

    @transaction.atomic
    def link_sub_category(
        self, request, linked_category: LinkedCategory, sub_category: SubCategory
    ) -> LinkedSubCategory:
        logger.debug("Linked sub-category: %s", sub_category.name)

        linked_sub_category = LinkedSubCategory()

        linked_sub_category.parent = sub_category
        linked_sub_category.category = linked_category

        linked_sub_category.full_clean()
        linked_sub_category.save()

        self.check_service.link_checks(
            request,
            linked_sub_category=linked_sub_category,
            sub_category=sub_category,
        )

        return linked_sub_category

    @transaction.atomic
    def update_sub_categories(
        self, request, linked_category: LinkedCategory, category: Category
    ) -> LinkedCategory:
        logger.debug("Updating sub-categories")

        for sub_category in category.sub_categories.all():
            logger.debug("Linked sub-category: %s", sub_category.name)
            # linked_sub_category = LinkedSubCategory()

            # linked_sub_category.parent = sub_category
            # linked_sub_category.category = linked_category

            # linked_sub_category.full_clean()
            # linked_sub_category.save()

            # self.check_service.link_checks(
            #     request,
            #     linked_sub_category=linked_sub_category,
            #     sub_category=sub_category,
            # )

        return linked_category

    @transaction.atomic
    def create(self, request, name: str, category: Category) -> SubCategory:
        """
        Saves a SubCategory object to the DB.
        """

        instance = SubCategory(
            category=category,
            name=name,
        )

        instance.full_clean()
        instance.save()

        return instance

    @transaction.atomic
    def update(self, request, instance: SubCategory, **fields) -> SubCategory:
        """
        Updates an existing SubCategory object in the DB.
        """

        instance.category = fields.get("category", instance.category)
        instance.name = fields.get("name", instance.name)

        instance.full_clean()
        instance.save()

        return instance
