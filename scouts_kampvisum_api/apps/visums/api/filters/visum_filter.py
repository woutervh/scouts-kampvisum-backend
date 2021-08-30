
from django_filters import rest_framework as filters

from ..models import CampVisum


class CampVisumFilter(filters.FilterSet):

    filter_group = 'uuid'

    class Meta:
        model = CampVisum
        fields = []
