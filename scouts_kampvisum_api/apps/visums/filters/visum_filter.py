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
        start_date = self.request.query_params.get("start_date", None)
        end_date = self.request.query_params.get("end_date", None)

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
        date_range_filter = Q()
        if start_date and end_date:
            date_range_filter = (Q(camp__year__start_date__lte=end_date)&Q(camp__year__end_date__gte=start_date))

        return parent.filter(and_condition).filter(date_range_filter).distinct()

        return parent.all()
