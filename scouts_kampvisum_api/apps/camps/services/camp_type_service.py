from typing import List

from django.utils import timezone
from django.core.exceptions import ValidationError

from apps.camps.models import CampType

from scouts_auth.inuits.utils import ListUtils

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampTypeService:
    def create(self, request, camp_type: str) -> CampType:
        """
        Saves a CampType object to the DB.
        """

        instance = CampType(
            camp_type=camp_type,
        )

        instance.created_by = request.user

        instance.full_clean()
        instance.save()

        return instance

    def update(self, request, instance: CampType, **fields) -> CampType:
        """
        Updates an existing CampType object in the DB.
        """

        instance.name = fields.get("camp_type", instance.camp_type)

        instance.updated_by = request.user
        instance.updated_on = timezone.now()

        instance.full_clean()
        instance.save()

        return instance

    def get_camp_types(
        self, camp_types: List[str] = None, include_default: bool = True
    ) -> List[CampType]:
        default_camp_type = [CampType.objects.get_default()]

        if camp_types is None or len(camp_types) == 0:
            # logger.warn("No camp types given, getting default CampType instance")

            if include_default:
                camp_types = default_camp_type
            else:
                camp_types = []
        else:
            camp_types = ListUtils.concatenate_unique_lists(
                default_camp_type if include_default else [],
                [
                    camp_type
                    if isinstance(camp_type, CampType)
                    else CampType.objects.safe_get(
                        camp_type=camp_type, raise_error=True
                    )
                    for camp_type in camp_types
                ],
            )

        if not camp_types or len(camp_types) == 0:
            raise ValidationError("Can't create a visum without camp types")

        return camp_types
