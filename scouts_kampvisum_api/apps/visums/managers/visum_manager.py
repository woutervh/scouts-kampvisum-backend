from typing import List

from django.conf import settings
from django.db import models, connections
from django.db.models import Q
from django.core.exceptions import ValidationError

from apps.camps.models import CampYear, CampType
from apps.groups.models import ScoutsSection

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

    def get_all_for_group_and_year(self, group_admin_id: str, year: int):
        with connections['default'].cursor() as cursor:
            cursor.execute(
                f"select vc.id as id, vc.group as group, vc.group_name as group_name, vc.name as name, cc.year as year from visums_campvisum vc left join camps_campyear cc on cc.id=vc.year_id where vc.group='{group_admin_id}'{' and cc.year={year}' if year else ''}"
            )
            return cursor.fetchall()
        return None

    def get_linked_groups(self):
        with connections['default'].cursor() as cursor:
            cursor.execute(
                f"select distinct(vc.group) as group, vc.group_name from visums_campvisum vc"
            )
            return cursor.fetchall()

    def count_unchecked_checks(self, pk):
        with connections['default'].cursor() as cursor:
            cursor.execute(
                f"select count(1) from visums_linkedcategoryset vl where vl.visum_id = '{pk}' and vl.check_state = 'UNCHECKED'"
            )
            return cursor.fetchone()[0]

        return 1


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
            if isinstance(group, ScoutsGroup):
                group_admin_id = group.group_admin_id
            else:
                group_admin_id = group
        if year:
            year = year.year

        if not group_admin_id:
            raise ValidationError(f"Can't query CampVisum without a group")

        from apps.visums.models import LinkedCategory

        results = self.get_queryset().get_all_for_group_and_year(
            group_admin_id=group_admin_id, year=year)

        visums = []
        for result in results:
            visums.append({
                "id": result[0],
                "group": result[1],
                "group_name": result[2],
                "name": result[3],
                "year": result[4] if year else None,
                "sections": ScoutsSection.objects.get_for_visum(
                    visum_id=result[0]),
                "camp_types": CampType.objects.get_for_visum(
                    visum_id=result[0]),
                "category_set": {
                    "categories": LinkedCategory.objects.get_for_visum(visum_id=result[0])
                }
            })
        return visums

    def has_unchecked_checks(self, pk):
        return True if self.get_queryset().count_unchecked_checks(pk=pk) == 0 else False
