import logging

from ..models import CampVisum
from ..services import LinkedCategoryService
from apps.camps.services import CampService
from apps.groups.api.models import Section


logger = logging.getLogger(__name__)


class CampVisumService():

    camp_service = CampService()

    def visum_create(self, **fields):
        logger.debug("Creating Campvisum with data: %s", fields)

        camp_data = fields.get('camp')
        camp_name = camp_data.get('name')

        logger.debug("Creating camp with name '%s'", camp_name)
        camp = self.camp_service.camp_create(**camp_data)

        logger.debug("Linking category set to camp '%s'", camp_name)
        category_set = LinkedCategoryService().link_category_set(camp)

        visum = CampVisum()

        visum.camp = camp
        visum.category_set = category_set

        visum.full_clean()
        visum.save()

        return visum

    def visum_update(self, instance: CampVisum, **fields) -> CampVisum:
        """
        Updates an existing CampVisum object in the DB.
        """
        camp = instance.camp
        camp_fields = fields.pop('camp')

        instance.camp = self.camp_service.camp_update(
            instance=camp, **camp_fields)

        instance.full_clean()
        instance.save()

        return instance
