import logging
from typing import List

from apps.camps.models import CampType

from scouts_auth.inuits.utils import ListUtils

logger = logging.getLogger(__name__)


class CampTypeService:
    def create(self, request, camp_type: str) -> CampType:
        """
        Saves a CampType object to the DB.
        """

        instance = CampType(
            camp_type=camp_type,
        )

        instance.full_clean()
        instance.save()

        return instance

    def update(self, request, instance: CampType, **fields) -> CampType:
        """
        Updates an existing CampType object in the DB.
        """

        instance.name = fields.get("camp_type", instance.camp_type)

        instance.full_clean()
        instance.save()

        return instance

    def load_camp_types(self, camp_types: List[str] = None) -> List[CampType]:
        default_camp_type = [CampType.objects.get_default()]

        if camp_types is None or len(camp_types) == 0:
            logger.warn("No camp type given, getting default CampType instance")
            camp_types = default_camp_type
        else:
            camp_types = ListUtils.concatenate_unique_lists(
                default_camp_type,
                [CampType.objects.get(name=name) for name in camp_types],
            )

        return camp_types
