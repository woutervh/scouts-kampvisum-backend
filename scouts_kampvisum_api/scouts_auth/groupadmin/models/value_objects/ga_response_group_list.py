from typing import List

from scouts_auth.groupadmin.models.value_objects import AbstractScoutsGroup, AbstractScoutsLink
from scouts_auth.inuits.models import AbstractNonModel


class AbstractScoutsGroupListResponse(AbstractNonModel):

    scouts_groups: List[AbstractScoutsGroup]
    links: List[AbstractScoutsLink]

    class Meta:
        abstract = True

    def __init__(self, scouts_groups: List[AbstractScoutsGroup] = None, links: List[AbstractScoutsLink] = None):
        self.scouts_groups = scouts_groups.sort(key=lambda group: group.group_admin_id) if scouts_groups else []
        self.links = links if links else []

        # super().__init__([], {})
