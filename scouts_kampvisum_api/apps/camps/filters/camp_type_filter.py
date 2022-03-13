from django_filters import rest_framework as filters
from django.db.models import Q

from apps.camps.models import CampType


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampTypeFilter(filters.FilterSet):
    class Meta:
        model = CampType
        fields = []

    @property
    def qs(self):
        return super().qs.all()
