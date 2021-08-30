import logging

from ..services import CampVisumLinkedCategoryService
from apps.camps.services import CampService


logger = logging.getLogger(__name__)


class CampVisumService():

    def create_visum(self):
        logger.debug("Creating camp with name '%s'", camp.name)
        camp = CampService().camp_create

        logger.debug("Linking category set to camp '%s'", camp.name)
        CampVisumLinkedCategoryService().link_category_set(camp)
