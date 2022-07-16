from django_filters import rest_framework as filters

from apps.groups.models import ScoutsSection


class ScoutsSectionFilter(filters.FilterSet):
    class Meta:
        model = ScoutsSection
        fields = []

    @property
    def qs(self):
        return super().qs.allowed(user=self.request.user).filter(hidden=False)
