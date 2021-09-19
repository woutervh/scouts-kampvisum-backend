import django_filters

from ..models import Group


class GroupFilter(django_filters.FilterSet):

    term = django_filters.CharFilter(method="search_term_filter")

    class Meta:
        model = Group
        fields = "__all__"

    def search_term_filter(self, queryset, name, value):
        # Annotate brand license so we can do an icontains on entire string
        return ()
