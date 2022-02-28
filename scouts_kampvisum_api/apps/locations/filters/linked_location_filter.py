import logging

from django.db.models import Q
from django_filters import FilterSet, CharFilter

from apps.locations.models import LinkedLocation


logger = logging.getLogger(__name__)


class LinkedLocationFilter(FilterSet):
    term = CharFilter(method="search_term_filter")

    class Meta:
        model = LinkedLocation
        fields = []

    def search_term_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
            | Q(contact_name__icontains=value)
            | Q(locations__name__icontains=value)
            | Q(locations__address__icontains=value)
        )
