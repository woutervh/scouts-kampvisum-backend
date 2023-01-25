from typing import List

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

from scouts_auth.groupadmin.models import AbstractScoutsFunction, ScoutsGroup
from scouts_auth.groupadmin.settings import GroupAdminSettings


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampVisumQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def allowed(self, user: settings.AUTH_USER_MODEL):
        from scouts_auth.groupadmin.services import ScoutsAuthorizationService
        service = ScoutsAuthorizationService()

        leader_functions: List[AbstractScoutsFunction] = service.get_active_leader_functions(
            user)

        group_admin_ids = GroupAdminSettings.get_administrator_groups()
        for leader_function in leader_functions:
            group_admin_ids.append(leader_function.scouts_group.group_admin_id)

            if user.has_role_district_commissioner() or user.has_role_shire_president():
                underlyingGroups: List[ScoutsGroup] = list(
                    ScoutsGroup.objects.get_groups_with_parent(
                        parent_group_admin_id=leader_function.scouts_group.group_admin_id
                    )
                )

                for underlyingGroup in underlyingGroups:
                    if leader_function.is_district_commissioner_for_group(scouts_group=underlyingGroup) or leader_function.is_shire_president_for_group(scouts_group=underlyingGroup):
                        group_admin_ids.append(
                            underlyingGroup.group_admin_id)

        return self.filter(group__group_admin_id__in=group_admin_ids)


class CampVisumManager(models.Manager):
    def get_queryset(self):
        return CampVisumQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate CampVisum instance(s) with the provided params: (id: {})".format(
                    pk,
                )
            )

        return None
