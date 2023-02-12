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
        group_admin_id = self.request.query_params.get("group", None)
        year = self.request.query_params.get("year", None)
        if not year or year == "undefined":
            year = CampYearService().get_or_create_current_camp_year()
            year = year.year

        return CampVisum.objects.get_all_for_group_and_year(group_admin_id=group_admin_id, year_number=year)
