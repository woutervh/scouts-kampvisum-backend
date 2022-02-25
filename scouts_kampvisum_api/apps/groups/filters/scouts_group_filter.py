from django_filters import rest_framework as filters

from scouts_auth.groupadmin.models import AbstractScoutsGroup


class ScoutsGroupFilter(filters.FilterSet):

    group = filters.CharFilter(method="search_group")

    class Meta:
        model = AbstractScoutsGroup
        fields = []

    @property
    def qs(self):
        return super().qs

    def search_group(self, queryset, name, value):
        # return self.qs.all()
        return []
