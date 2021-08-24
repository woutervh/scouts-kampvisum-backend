import logging, uuid
from django_filters import rest_framework as filters
from django.db.models import Q

from .models import ScoutsCamp


logger = logging.getLogger(__name__)


class ScoutsCampAPIFilter(filters.FilterSet):

    filter_group = 'uuid'

    class Meta:
        model = ScoutsCamp
        fields = [  ]
    
    # def filter_group(self, queryset, name, group):
    #     return queryset.filter(Q(sections__group__uuid=group))
    
    # def filter_year(self, queryset, name, year):
    #     return queryset.filter(Q(start_date__year=year))

    @property
    def qs(self):
        parent = super().qs
        group = self.request.query_params.get('group', None)
        year = self.request.query_params.get('year', None)

        if group and self.filter_group == 'uuid':
            group = uuid.UUID(group)

        logger.debug('Filtering with group %s and year %s', group, year)

        #return parent.filter(Q(sections__group__uuid=group), Q(start_date__year=year))
        if year and group:
            if self.filter_group == 'uuid':
                return parent.filter(
                    Q(start_date__year=year),
                    Q(sections__group__uuid=group)).distinct()
            else:
                return parent.filter(
                    Q(start_date__year=year),
                    Q(sections__group__id=group)).distinct()
        else:
            if year:
                return parent.filter(start_date__year=year)
            if group:
                if self.filter_group == 'uuid':
                    return parent.filter(
                        sections__group__uuid=group).distinct()
                else:
                    return parent.filter(
                        sections__group__id=group).distinct()
        
        return parent.all()



class ScoutsCampFilter(ScoutsCampAPIFilter):

    filter_group = 'pk'

