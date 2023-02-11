from typing import List

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError

from apps.camps.models import CampYear

from scouts_auth.groupadmin.models import AbstractScoutsFunction, ScoutsGroup
from scouts_auth.groupadmin.settings import GroupAdminSettings


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampVisumQuerySet(models.QuerySet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def all(self, *args, **kwargs):
        return super().all(*args, **kwargs)

    def get_for_group(self, group_admin_id: str):
        return super().filter(group=group_admin_id)

    def get_for_year(self, year: int):
        return super().filter(year__year=year)

    def get_for_group_and_year(self, group_admin_id: str, year: int):
        return super().filter(group=group_admin_id, year__year=year)


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

    def get_for_group_and_year(self, group: ScoutsGroup = None, group_admin_id: str = None, year: CampYear = None, year_number: int = None):
        if group:
            group_admin_id = group.group_admin_id
        if year:
            year = year.year

        if group_admin_id and year:
            return self.get_queryset().get_for_group_and_year(group_admin_id=group_admin_id, year=year)

        if group_admin_id:
            return self.get_queryset().get_for_group(group_admin_id=group_admin_id)

        if year:
            return self.get_queryset().get_for_year(year=year)
