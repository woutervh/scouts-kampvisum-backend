from typing import List

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

from scouts_auth.groupadmin.models import ScoutsFunction, ScoutsGroup


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsSectionQuerySet(models.QuerySet):
    def allowed(self, user: settings.AUTH_USER_MODEL):
        leader_functions: List[ScoutsFunction] = list(
            ScoutsFunction.objects.get_leader_functions(user=user)
        )

        group_admin_ids = []
        for leader_function in leader_functions:
            for group in leader_function.scouts_groups:
                group_admin_ids.append(group.group_admin_id)

                if user.has_role_district_commissioner():
                    underlyingGroups: List[ScoutsGroup] = list(
                        ScoutsGroup.objects.get_groups_with_parent(
                            parent_group_admin_id=group.group_admin_id
                        )
                    )

                    for underlyingGroup in underlyingGroups:
                        if leader_functions.is_district_commissioner_for_group(scouts_group=underlyingGroup):
                            group_admin_ids.append(
                                underlyingGroup.group_admin_id)

        return self.filter(group__group_admin_id__in=group_admin_ids)


class ScoutsSectionManager(models.Manager):
    def get_queryset(self):
        return ScoutsSectionQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        name = kwargs.get("name", None)
        gender = kwargs.get("gender", None)
        age_group = kwargs.get("age_group", None)
        group = kwargs.get("group", None)
        group_group_admin_id = kwargs.get("group_group_admin_id", None)
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if name and gender and age_group:
            if group:
                try:
                    return self.get_queryset().get(
                        group=group, name=name, gender=gender, age_group=age_group
                    )
                except:
                    pass

            if group_group_admin_id:
                try:
                    return self.get_queryset().get(
                        group__group_admin_id=group_group_admin_id,
                        name=name,
                        gender=gender,
                        age_group=age_group,
                    )
                except:
                    pass

        if raise_error:
            raise ValidationError(
                "Unable to locate ScoutsSection instance with the provided params: (pk: ({}), (group: ({}), name: ({}), gender: ({}), age_group: ({})), (group_group_admin_id: ({}), name ({}), gender({}), age_group({})))".format(
                    pk,
                    group,
                    name,
                    gender,
                    age_group,
                    group_group_admin_id,
                    name,
                    gender,
                    age_group,
                )
            )
        return None

    def get_by_natural_key(self, group, name, gender, age_group):
        logger.trace(
            "GET BY NATURAL KEY %s: (group: %s (%s), name: %s (%s), gender: %s (%s), age_group: %s (%s))",
            "ScoutsSection",
            group,
            type(group).__name__,
            name,
            type(name).__name__,
            gender,
            type(gender).__name__,
            age_group,
            type(age_group).__name__,
        )

        if isinstance(group, ScoutsGroup):
            return self.get(group=group, name=name, gender=gender, age_group=age_group)

        return self.get(
            group__group_admin_id=group, name=name, gender=gender, age_group=age_group
        )
