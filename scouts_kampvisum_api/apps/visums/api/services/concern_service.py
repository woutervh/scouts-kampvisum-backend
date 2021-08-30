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

        concerns = instance.concerns.all()
        for concern in concerns:
            concern_service.deepcopy(concern)

        return instance_copy
