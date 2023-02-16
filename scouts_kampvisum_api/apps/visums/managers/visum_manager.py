from typing import List

from django.conf import settings
from django.db import models, connections
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

    def get_all_for_group(self, group_admin_id: str):
        return super().filter(group=group_admin_id)

    def get_all_for_year(self, year: int):
        return super().filter(year__year=year)

    def get_all_for_group_and_year(self, group_admin_id: str, year: int):
        with connections['default'].cursor() as cursor:
            cursor.execute(
                f"select * from visums_campvisum vc left join camps_campyear cc on cc.id=vc.year_id where vc.group={group_admin_id} and cc.year={year}"
            )
            return cursor.fetchall()
        return super().filter(group=group_admin_id, year__year=year)

    def get_linked_groups(self):
        with connections['default'].cursor() as cursor:
            cursor.execute(
                f"select distinct(vc.group) as group, vc.group_name from visums_campvisum vc"
            )
            return cursor.fetchall()


class CampVisumManager(models.Manager):
    def get_queryset(self):
        return CampVisumQuerySet(self.model, using=self._db).prefetch_related('category_set', 'year', 'sections', 'camp_types', 'engagement')

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except Exception:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate CampVisum instance(s) with the provided params: (id: {})".format(
                    pk,
                )
            )

        return None

    def get_all_for_group_and_year(self, group: ScoutsGroup = None, group_admin_id: str = None, year: CampYear = None, year_number: int = None):
        if group:
            group_admin_id = group.group_admin_id
        if year:
            year = year.year

        if group_admin_id and year:
            return self.get_queryset().get_all_for_group_and_year(group_admin_id=group_admin_id, year=year)

        if group_admin_id:
            return self.get_queryset().get_all_for_group(group_admin_id=group_admin_id)

        if year:
            return self.get_queryset().get_all_for_year(year=year)

    def get_linked_groups(self) -> List[ScoutsGroup]:
        result = self.get_queryset().get_linked_groups()

        logger.debug(f"KNOWN GROUPS: {result}")
