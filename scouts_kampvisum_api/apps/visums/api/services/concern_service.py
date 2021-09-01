import logging
import copy

from ..models import Concern


logger = logging.getLogger(__name__)


class ConcernService():

    def deepcopy(self,
                 instance: Concern) -> Concern:
        concern_service = ConcernService()
        instance_copy = copy.deepcopy(instance)

        instance_copy.full_clean()
        instance_copy.save()

        concerns = instance.concerns.all()
        for concern in concerns:
            concern_service.deepcopy(concern)

        return instance_copy
