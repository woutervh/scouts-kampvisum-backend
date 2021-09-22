import logging

from ..models import Concern
from inuits import copy_basemodel


logger = logging.getLogger(__name__)


class ConcernService:
    def deepcopy(self, instance: Concern) -> Concern:
        instance_copy = copy_basemodel(instance)
        instance_copy.is_default = False

        instance_copy.full_clean()
        instance_copy.save()

        return instance_copy
