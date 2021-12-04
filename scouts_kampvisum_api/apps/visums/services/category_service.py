import logging

from apps.visums.services import SubCategoryService
from apps.visums.models import Category

logger = logging.getLogger(__name__)


class CategoryService:
    def create(self, *, name: str) -> Category:
        """
        Saves a Category object to the DB.
        """

        instance = Category(
            name=name,
        )

        instance.full_clean()
        instance.save()

        return instance

    def update(self, *, instance: Category, **fields) -> Category:
        """
        Updates an existing Category object in the DB.
        """

        instance.name = fields.get("name", instance.name)

        instance.full_clean()
        instance.save()

        return instance

    def deepcopy(self, instance: Category) -> Category:
        sub_category_service = SubCategoryService()

        instance_copy = copy_basemodel(instance)
        instance_copy.is_default = False

        instance_copy.full_clean()
        instance_copy.save()

        sub_categories = instance.sub_categories.all()
        for sub_category in sub_categories:
            sub_category_copy = sub_category_service.deepcopy(sub_category)
            instance_copy.sub_categories.add(sub_category_copy)

        return instance_copy
