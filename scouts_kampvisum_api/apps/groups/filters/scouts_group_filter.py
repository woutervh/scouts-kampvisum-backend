import django_filters

from scouts_auth.groupadmin.models import AbstractScoutsGroup


class ScoutsGroupFilter(django_filters.FilterSet):

    group = django_filters.CharFilter(method="search_group")

    class Meta:
        model = AbstractScoutsGroup
        fields = "__all__"

    def search_group(self, queryset, name, value):

        return ()
