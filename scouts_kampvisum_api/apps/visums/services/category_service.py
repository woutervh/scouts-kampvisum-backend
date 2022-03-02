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
    def create_linked_categories(
        self,
        request,
        linked_category_set: LinkedCategorySet,
    ) -> LinkedCategorySet:
        categories: List[Category] = self.get_categories(
            camp_year=linked_category_set.visum.camp.year,
            camp_types=linked_category_set.visum.camp_types.all(),
        )
        logger.debug(
            "Linking %d Category instances for camp_year %d and camp_types %s to visum %s",
            len(categories),
            linked_category_set.visum.camp.year.year,
            ",".join(
                camp_type.camp_type
                for camp_type in linked_category_set.visum.camp_types.all()
            ),
            linked_category_set.visum.camp.name,
        )

        for category in categories:
            self.create_linked_category(
                request=request,
                linked_category_set=linked_category_set,
                category=category,
            )

        return linked_category_set

    @transaction.atomic
    def create_linked_category(
        self, request, linked_category_set: LinkedCategorySet, category: Category
    ) -> LinkedCategory:
        logger.debug(
            "Linking category %s to LinkedCategorySet with id %s",
            category.name,
            linked_category_set.id,
        )

        linked_category = LinkedCategory()

        linked_category.parent = category
        linked_category.category_set = linked_category_set

        linked_category.full_clean()
        linked_category.save()

        self.sub_category_service.link_sub_categories(
            request, linked_category=linked_category, category=category
        )

        return linked_category

    @transaction.atomic
    def update_linked_categories(
        self,
        request,
        linked_category_set: LinkedCategorySet,
        categories: List[Category],
    ) -> LinkedCategorySet:
        categories: List[Category] = self.get_categories(
            camp_year=linked_category_set.visum.camp.year,
            camp_types=linked_category_set.visum.camp_types.all(),
        )
        logger.debug(
            "Found %d Category instances for camp_year %d and camp_types %s to update for visum %s",
            len(categories),
            linked_category_set.visum.camp.year.year,
            ",".join(
                camp_type.camp_type
                for camp_type in linked_category_set.visum.camp_types.all()
            ),
            linked_category_set.visum.camp.name,
        )

        current_categories: List[Category] = linked_category_set.categories.all()
        logger.debug(
            "Found %d Category instance(s) currently linked to set",
            len(current_categories),
        )

        # A category can be added, updated or removed from the fixture
        for category in categories:
            logger.debug("Updating category: '%s'", category.name)

            linked_category: LinkedCategory = LinkedCategory.objects.safe_get(
                category=category
            )

            # Added Category
            if not linked_category:
                linked_category: LinkedCategory = self.create_linked_category(
                    request=request,
                    linked_category_set=linked_category_set,
                    category=category,
                )
            # Updated Category
            else:
                self.update_linked_category(
                    request=request, instance=linked_category, category=category
                )

        # Deleted Category

        return linked_category_set

    @transaction.atomic
    def update_linked_category(
        self, request, instance: LinkedCategory, category: Category
    ) -> LinkedCategory:
        self.sub_category_service.update_sub_categories(
            request, linked_category=instance, category=category
        )

        return instance

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
