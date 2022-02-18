import logging

from django_filters import rest_framework as filters
from django.db.models import Q

from apps.visums.models import CampVisum

from apps.camps.services import CampYearService


logger = logging.getLogger(__name__)


class CampVisumFilter(filters.FilterSet):
    class Meta:
        model = CampVisum
        fields = []

    @property
    def qs(self):
        parent = super().qs

        group_admin_id = self.request.query_params.get("group", None)
        year = self.request.query_params.get("year", None)

        if not year or year == "undefined":
            year = CampYearService().get_or_create_current_camp_year()

            year = year.year

        if year and group_admin_id:
            logger.debug(
                "Filtering CampVisum instances with group %s and year %s",
                group_admin_id,
                year,
            )
            return (
                parent.filter(
                    Q(camp__year__year=year),
                    Q(camp__sections__group_group_admin_id=group_admin_id),
                )
                # .order_by("camp__sections__name__age_group")
                # .distinct("camp__sections__name__age_group")
                .distinct()
            )
        if year:
            logger.debug("Filtering CampVisum instances with year %s", year)
            return (
                parent.filter(camp__year__year=year)
                # .order_by("camp__sections__name__age_group")
                # .distinct("camp__sections__name__age_group")
                .distinct()
            )
        if group_admin_id:
            logger.debug("Filtering CampVisum instances with group %s", group_admin_id)
            result = (
                parent.filter(Q(camp__sections__group_group_admin_id=group_admin_id))
                # .order_by("camp__sections__name__age_group")
                # .distinct("camp__sections__name__age_group")
                .distinct()
            )
            logger.debug(
                "Found %d CampVisum instances for group %s",
                result.count(),
                group_admin_id,
            )
            return result

        logger.debug("Filters for CampVisum not set, returning all instances")
        return parent.all()
