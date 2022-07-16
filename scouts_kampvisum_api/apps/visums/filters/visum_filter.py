from django_filters import rest_framework as filters
from django.db.models import Q

from apps.visums.models import CampVisum

from apps.camps.services import CampYearService

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


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

        query_filters = dict()
        if group_admin_id:
            query_filters["group__group_admin_id"] = group_admin_id
        if year:
            query_filters["camp__year__year"] = year

        and_condition = Q()
        for key, value in query_filters.items():
            and_condition.add(Q(**{key: value}), Q.AND)

        return parent.allowed(user=self.request.user).filter(and_condition).distinct()
