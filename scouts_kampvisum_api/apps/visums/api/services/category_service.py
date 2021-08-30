import logging
import copy
from ..services import CampVisumSubCategoryService
from ..models import CampVisumCategory


logger = logging.getLogger(__name__)


class CampVisumCategoryService():

    def create(
            self, *, name: str) -> CampVisumCategory:
        """
        Saves a CampVisumCategory object to the DB.
        """

        instance = CampVisumCategory(
            name=name,
        )

        instance.full_clean()
        instance.save()

        return instance

    def update(
            self,
            *,
            instance: CampVisumCategory,
            **fields) -> CampVisumCategory:
        """
        Updates an existing CampVisumCategory object in the DB.
        """

        instance.name = fields.get('name', instance.name)

        instance.full_clean()
        instance.save()

        return instance

    def deepcopy(self, instance: CampVisumCategory) -> CampVisumCategory:
        sub_category_service = CampVisumSubCategoryService()
        instance_copy = copy.deepcopy(instance)

        instance_copy.full_clean()
        instance_copy.save()

        sub_categories = instance.sub_categories.all()
        for sub_category in sub_categories:
            sub_category_copy = sub_category_service.deepcopy(sub_category)
            instance_copy.sub_categories.add(sub_category_copy)

        return instance_copy
