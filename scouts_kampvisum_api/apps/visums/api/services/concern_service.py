import logging
import copy

from ..models import CampVisumConcern


logger = logging.getLogger(__name__)


class CampVisumConcernService():

    def deepcopy(self,
                 instance: CampVisumConcern) -> CampVisumConcern:
        concern_service = CampVisumConcernService()
        instance_copy = copy.deepcopy(instance)

        instance_copy.full_clean()
        instance_copy.save()

        return instance_copy
