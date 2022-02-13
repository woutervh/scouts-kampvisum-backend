import logging

from apps.camps.services import CampService

from apps.deadlines.services import DeadlineService

from apps.visums.models import LinkedCategorySet, CampVisum
from apps.visums.services import CategorySetService


logger = logging.getLogger(__name__)


class CampVisumService:

    camp_service = CampService()
    category_set_service = CategorySetService()
    deadline_service = DeadlineService()

    def visum_create(self, request, **data) -> CampVisum:
        logger.debug("Creating Campvisum with data: %s", data)

        camp_data = data.get("camp", {})
        camp_name = camp_data.get("name", None)

        logger.debug("Creating camp with name '%s'", camp_name)
        camp = self.camp_service.camp_create(request, **camp_data)

        logger.debug("Linking category set to visum")
        category_set: LinkedCategorySet = (
            self.category_set_service.get_linked_category_set(request, camp)
        )

        visum = CampVisum()

        visum.camp = camp
        visum.category_set = category_set

        visum.full_clean()
        visum.save()

        logger.debug("Linking default deadline set to visum")
        self.deadline_service.link_to_visum(request=request, visum=visum)

        return visum

    def visum_update(self, request, instance: CampVisum, **fields) -> CampVisum:
        """
        Updates an existing CampVisum object in the DB.
        """
        camp = instance.camp
        camp_fields = fields.pop("camp")

        instance.camp = self.camp_service.camp_update(
            request, instance=camp, **camp_fields
        )

        instance.full_clean()
        instance.save()

        # existing_camp_types = instance.category_set.parent.camp_type
        camp_types = fields.get("camp_types", [])

        return instance
