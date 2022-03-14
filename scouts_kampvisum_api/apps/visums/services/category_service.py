from typing import List

from django.db import transaction

from apps.camps.models import CampYear, CampType

from apps.visums.models import Category
from apps.visums.services import SubCategoryService


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CategoryService:

    sub_category_service = SubCategoryService()

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
