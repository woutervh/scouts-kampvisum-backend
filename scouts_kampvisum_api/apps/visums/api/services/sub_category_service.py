import logging

from ..models import Category, SubCategory
from ..services import ConcernService
from inuits import copy_basemodel

logger = logging.getLogger(__name__)


class SubCategoryService:
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

    def deepcopy(self, instance: SubCategory) -> SubCategory:
        concern_service = ConcernService()
        instance_copy = copy_basemodel(instance)
        instance_copy.is_default = False

        instance_copy.full_clean()
        instance_copy.save()

        concerns = instance.concerns.all()
        for concern in concerns:
            concern_copy = concern_service.deepcopy(concern)
            instance_copy.concerns.add(concern_copy)

        return instance_copy
