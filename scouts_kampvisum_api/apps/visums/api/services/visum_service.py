import logging

from ..models import CampVisum
from ..services import CampVisumLinkedCategoryService
from apps.camps.services import CampService


logger = logging.getLogger(__name__)


class CampVisumService():

    def visum_create(self, **fields):
        logger.debug("Creating Campvisum with data: %s", fields)

        camp_data = fields.get('camp')
        camp_name = camp_data.get('name')

        logger.debug("Creating camp with name '%s'", camp_name)
        camp = CampService().camp_create(**camp_data)

        logger.debug("Linking category set to camp '%s'", camp_name)
        category_set = CampVisumLinkedCategoryService().link_category_set(camp)

        visum = CampVisum()

        visum.camp = camp
        visum.category_set = category_set

        visum.full_clean()
        visum.save()

        return visum
