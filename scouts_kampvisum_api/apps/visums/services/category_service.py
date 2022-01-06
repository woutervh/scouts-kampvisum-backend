import logging

from apps.visums.models import LinkedCategorySet, CategorySet, LinkedCategory, Category
from apps.visums.services import SubCategoryService

logger = logging.getLogger(__name__)


class CategoryService:

    # category_set_service = CategorySetService()
    sub_category_service = SubCategoryService()

    def link_categories(
        self, request, linked_category_set: LinkedCategorySet, category_set: CategorySet
    ) -> LinkedCategorySet:
        logger.debug("Linking categories")

        for category in category_set.categories.all():
            logger.debug("Linked category: '%s'", category.name)

            linked_category = LinkedCategory()

            linked_category.parent = category
            linked_category.category_set = linked_category_set

            linked_category.full_clean()
            linked_category.save()

            self.sub_category_service.link_sub_categories(
                request, linked_category=linked_category, category=category
            )

        return linked_category_set

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

    def update(self, request, instance: Category, **fields) -> Category:
        """
        Updates an existing Category object in the DB.
        """

        instance.name = fields.get("name", instance.name)

        instance.full_clean()
        instance.save()

        return instance

    # def deepcopy(self, instance: Category) -> Category:
    #     sub_category_service = SubCategoryService()

    #     instance_copy = copy_basemodel(instance)
    #     instance_copy.is_default = False

    #     instance_copy.full_clean()
    #     instance_copy.save()

    #     sub_categories = instance.sub_categories.all()
    #     for sub_category in sub_categories:
    #         sub_category_copy = sub_category_service.deepcopy(sub_category)
    #         instance_copy.sub_categories.add(sub_category_copy)

    #     return instance_copy
