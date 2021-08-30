import logging
import copy

from ..models import (
    CampVisumCategory,
    CampVisumSubCategory
)
from ..services import CampVisumConcernService


logger = logging.getLogger(__name__)


class CampVisumSubCategoryService():

    def create(
            self, *,
            name: str,
            category: CampVisumCategory) -> CampVisumSubCategory:
        """
        Saves a CampVisumSubCategory object to the DB.
        """

        instance = CampVisumSubCategory(
            category=category,
            name=name,
        )

        instance.full_clean()
        instance.save()

        return instance

    def update(
            self,
            *,
            instance: CampVisumSubCategory,
            **fields) -> CampVisumSubCategory:
        """
        Updates an existing CampVisumSubCategory object in the DB.
        """

        instance.category = fields.get('category', instance.category)
        instance.name = fields.get('name', instance.name)

        instance.full_clean()
        instance.save()

        return instance

    def deepcopy(self,
                 instance: CampVisumSubCategory) -> CampVisumSubCategory:
        concern_service = CampVisumConcernService()
        instance_copy = copy.deepcopy(instance)

        instance_copy.full_clean()
        instance_copy.save()

        concerns = instance.concerns.all()
        for concern in concerns:
            concern_copy = concern_service.deepcopy(concern)
            instance_copy.concerns.add(concern_copy)

        return instance_copy
