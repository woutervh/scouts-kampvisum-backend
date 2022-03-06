from django_filters import FilterSet, CharFilter

from scouts_auth.inuits.models import PersistedFile

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class PersistedFileFilter(FilterSet):
    term = CharFilter(method="search_term_filter")

    class Meta:
        model = PersistedFile
        fields = []

    def search_term_filter(self, queryset, name, value):
        # Annotate full name so we can do an icontains on the entire name
        return queryset.filter(file__icontains=value)
