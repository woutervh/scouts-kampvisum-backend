import logging
from typing import List

from django.db import transaction

from apps.camps.models import CampYear, CampType

from apps.visums.models import LinkedCategorySet, LinkedCategory, Category
from apps.visums.services import SubCategoryService

logger = logging.getLogger(__name__)


class CategoryService:

    sub_category_service = SubCategoryService()

    def get_categories(
        self, camp_year: CampYear, camp_types: List[CampType]
    ) -> List[Category]:
        return Category.objects.safe_get(
            camp_year=camp_year, camp_types=camp_types, raise_error=True
        )

    @transaction.atomic
    def link_categories(
        self,
        request,
        linked_category_set: LinkedCategorySet,
        categories: List[Category],
    ) -> LinkedCategorySet:
        logger.debug(
            "Linking %d categories to visum %s",
            len(categories),
            linked_category_set.visum.camp.name,
        )

        for category in categories:
            logger.debug("Linking category: '%s'", category.name)

            linked_category = LinkedCategory()

            linked_category.parent = category
            linked_category.category_set = linked_category_set

            linked_category.full_clean()
            linked_category.save()

            self.sub_category_service.link_sub_categories(
                request, linked_category=linked_category, category=category
            )

        return linked_category_set

    @transaction.atomic
    def create(self, request, name: str) -> Category:
        """
        Saves a Category object to the DB.
        """

        instance = Category(
            name=name,
        )

        instance.full_clean()
        instance.save()

        return instance

    @transaction.atomic
    def update(self, request, instance: Category, **fields) -> Category:
        """
        Updates an existing Category object in the DB.
        """

        instance.name = fields.get("name", instance.name)

        instance.full_clean()
        instance.save()

        return instance
