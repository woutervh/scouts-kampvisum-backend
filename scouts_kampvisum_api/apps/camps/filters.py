import logging, uuid

from django_filters import rest_framework as filters
from django.db.models import Q

from apps.camps.models import Camp


logger = logging.getLogger(__name__)


class CampAPIFilter(filters.FilterSet):

    filter_group = "uuid"

    class Meta:
        model = Camp
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
                "Filtering Camp instances with group %s and year %s", group, year
            )
            if self.filter_group == "uuid":
                return parent.filter(
                    Q(start_date__year=year), Q(sections__group__uuid=group)
                ).distinct()
            else:
                return parent.filter(
                    Q(start_date__year=year), Q(sections__group__id=group)
                ).distinct()
        if year:
            logger.debug("Filtering Camp instances with year %s", year)
            return parent.filter(start_date__year=year)
        if group:
            logger.debug("Filtering Camp instances with group %s", group)
            if self.filter_group == "uuid":
                return parent.filter(sections__group__uuid=group).distinct()
            else:
                return parent.filter(sections__group__id=group).distinct()

        logger.debug("Filters for Camp not set, returning all instances")
        return parent.all()


class CampFilter(CampAPIFilter):

    filter_group = "pk"
