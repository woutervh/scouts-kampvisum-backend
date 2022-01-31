import logging

from apps.visums.models import CampType

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