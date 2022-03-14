from django.db import transaction

from apps.visums.models import Category, SubCategory


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class SubCategoryService:
    @transaction.atomic
    def create(self, request, name: str, category: Category) -> SubCategory:
        """
        Saves a SubCategory object to the DB.
        """

        instance = SubCategory()

        instance.category = (category,)
        instance.name = name

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
