import logging

from apps.visums.models import LinkedCategory, Category, LinkedSubCategory, SubCategory
from apps.visums.services import CheckService

logger = logging.getLogger(__name__)


class SubCategoryService:
    check_service = CheckService()

    def link_sub_categories(
        self, request, linked_category: LinkedCategory, category: Category
    ) -> LinkedCategory:
        logger.debug("Linking sub-categories")

        for sub_category in category.sub_categories.all():
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

        return linked_category

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

    def update(self, request, instance: SubCategory, **fields) -> SubCategory:
        """
        Updates an existing SubCategory object in the DB.
        """

        instance.category = fields.get("category", instance.category)
        instance.name = fields.get("name", instance.name)

        instance.full_clean()
        instance.save()

        return instance
