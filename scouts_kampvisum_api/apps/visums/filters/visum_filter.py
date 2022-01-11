import logging, uuid

from django_filters import rest_framework as filters
from django.db.models import Q

from apps.visums.models import CampVisum


logger = logging.getLogger(__name__)


class CampVisumAPIFilter(filters.FilterSet):
    class Meta:
        model = CampVisum
        fields = []

    @property
    def qs(self):
        parent = super().qs

        group_admin_id = self.request.query_params.get("group", None)
        year = self.request.query_params.get("year", None)

        if year and group_admin_id:
            logger.debug(
                "Filtering CampVisum instances with group %s \
                and year %s",
                group_admin_id,
                year,
            )
            return parent.filter(
                Q(camp__start_date__year=year),
                Q(camp__sections__group_admin_id=group_admin_id),
            ).distinct()
        if year:
            logger.debug("Filtering CampVisum instances with year %s", year)
            return parent.filter(camp__start_date__year=year).distinct()
        if group_admin_id:
            logger.debug("Filtering CampVisum instances with group %s", group_admin_id)
            result = parent.filter(
                Q(camp__sections__group_admin_id=group_admin_id)
            ).distinct()
            logger.debug(
                "Found %d CampVisum instances for group %s",
                result.count(),
                group_admin_id,
            )
            return result

        logger.debug("Filters for CampVisum not set, returning all instances")
        return parent.all()


class CampVisumFilter(filters.FilterSet):
    class Meta:
        model = CampVisum
        fields = []
