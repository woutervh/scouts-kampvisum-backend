import logging

from apps.visums.models import Category, SubCategory
from apps.visums.services import CheckService

logger = logging.getLogger(__name__)


class SubCategoryService:
    check_service = CheckService()

    def create(self, *, name: str, category: Category) -> SubCategory:
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

    def update(self, *, instance: SubCategory, **fields) -> SubCategory:
        """
        Updates an existing SubCategory object in the DB.
        """

        instance.category = fields.get("category", instance.category)
        instance.name = fields.get("name", instance.name)

        instance.full_clean()
        instance.save()

        return instance

    # def deepcopy(self, instance: SubCategory) -> SubCategory:
    #     instance_copy = copy_basemodel(instance)
    #     instance_copy.is_default = False

    #     instance_copy.full_clean()
    #     instance_copy.save()

    #     checks = instance.checks.all()
    #     for check in checks:
    #         check_copy = self.check_service.deepcopy(check)
    #         instance_copy.checks.add(check_copy)

    #     return instance_copy
