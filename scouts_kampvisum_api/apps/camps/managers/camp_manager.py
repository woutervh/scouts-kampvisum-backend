from typing import List

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

from scouts_auth.groupadmin.models import ScoutsFunction, ScoutsGroup


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def allowed(self, user: settings.AUTH_USER_MODEL):
        leader_functions: List[ScoutsFunction] = list(
            ScoutsFunction.objects.get_leader_functions(user=user)
        )

        group_admin_ids = []
        for leader_function in leader_functions:
            for group in leader_function.scouts_groups.all():
                group_admin_ids.append(group.group_admin_id)

                if user.has_role_district_commissioner():
                    underlyingGroups: List[ScoutsGroup] = list(
                        ScoutsGroup.objects.get_groups_with_parent(
                            parent_group_admin_id=group.group_admin_id
                        )
                    )

                    for underlyingGroup in underlyingGroups:
                        if leader_functions.is_district_commissioner_for_group(scouts_group=underlyingGroup):
                            group_admin_ids.append(underlyingGroup.group_admin_id)

        return self.filter(visum__group__group_admin_id__in=group_admin_ids)


class CampManager(models.Manager):
    """
    Loads CampYear instances by their integer year, not their id/uuid.

    This is useful for defining fixtures.
    """

    def get_queryset(self):
        return CampQuerySet(self.model, using=self._db)
