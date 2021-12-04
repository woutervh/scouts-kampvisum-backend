import logging, uuid

from django_filters import rest_framework as filters
from django.db.models import Q

from apps.visums.models import CampVisum


logger = logging.getLogger(__name__)


class CampVisumAPIFilter(filters.FilterSet):

    filter_group = "uuid"

    class Meta:
        model = CampVisum
        fields = []

    @property
    def qs(self):
        parent = super().qs
        group = self.request.query_params.get("group", None)
        year = self.request.query_params.get("year", None)

        if group and self.filter_group == "uuid":
            group = uuid.UUID(group)

        if year and group:
            logger.debug(
                "Filtering CampVisum instances with group %s \
                and year %s",
                group,
                year,
            )
            if self.filter_group == "uuid":
                return parent.filter(
                    Q(camp__start_date__year=year), Q(camp__sections__group__uuid=group)
                ).distinct()
            else:
                return parent.filter(
                    Q(camp__start_date__year=year), Q(camp__sections__group__id=group)
                ).distinct()
        if year:
            logger.debug("Filtering CampVisum instances with year %s", year)
            return parent.filter(camp__start_date__year=year)
        if group:
            logger.debug("Filtering CampVisum instances with group %s", group)
            if self.filter_group == "uuid":
                return parent.filter(camp__sections__group__uuid=group).distinct()
            else:
                return parent.filter(camp__sections__group__id=group).distinct()

        logger.debug("Filters for CampVisum not set, returning all instances")
        return parent.all()


class CampVisumFilter(filters.FilterSet):

    filter_group = "uuid"

    class Meta:
        model = CampVisum
        fields = []
