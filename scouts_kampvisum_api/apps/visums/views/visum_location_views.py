from datetime import datetime

from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema


from apps.visums.models import CampVisum
from apps.visums.filters import CampVisumFilter
from apps.visums.services import CampVisumService
from apps.locations.models import CampLocation
from apps.locations.serializers import CampLocationMinimalSerializer
from apps.camps.serializers import CampMinimalSerializer
from apps.visums.models import LinkedCategory
from apps.visums.models import LinkedSubCategory
from apps.visums.models import LinkedLocationCheck
from apps.camps.models.camp_year import CampYear

from scouts_auth.scouts.permissions import ScoutsFunctionPermissions
from scouts_auth.groupadmin.serializers.scouts_group_serializer import (
    ScoutsGroupSerializer,
)
from scouts_auth.groupadmin.models.scouts_group import ScoutsGroup
from scouts_auth.groupadmin.models.scouts_user import ScoutsUser

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger


logger: InuitsLogger = logging.getLogger(__name__)


class CampVisumLocationViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing camp location.
    """

    serializer_class = CampLocationMinimalSerializer
    queryset = CampVisum.objects.all()
    permission_classes = (ScoutsFunctionPermissions,)
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CampVisumFilter

    camp_visum_service = CampVisumService()

    @swagger_auto_schema(responses={status.HTTP_200_OK: CampLocationMinimalSerializer})
    def list(self, request):
        # HACKETY HACK
        # This should probably be handled by a rest call when changing groups in the frontend,
        # but adding it here avoids the need for changes to the frontend

        user: ScoutsUser = request.user
        group_admin_id = self.request.GET.get("group", None)
        year: int = self.request.GET.get("year")
        year: CampYear = CampYear.objects.get(year=year)

        if group_admin_id == "any":
            campvisums = set(CampVisum.objects.all().filter(year=year))
        else:
            campvisums = set(
                CampVisum.objects.all().filter(group=group_admin_id, year=year)
            )

        locations = list()
        date_in_range = True

        if request.query_params.get("start_date"):
            start_date = datetime.strptime(
                request.query_params.get("start_date"),
                "%Y-%m-%d",
            ).date()
        else:
            start_date = None

        if request.query_params.get("end_date"):
            end_date = datetime.strptime(
                request.query_params.get("end_date"),
                "%Y-%m-%d",
            ).date()
        else:
            end_date = None

        for campvisum in campvisums:
            group: ScoutsGroup = user.get_scouts_group(campvisum.group)
            if start_date and end_date:
                date_in_range = False
                if (campvisum.start_date and campvisum.start_date >= start_date) and (
                    campvisum.end_date and campvisum.end_date <= end_date
                ):
                    date_in_range = True
            elif start_date:
                date_in_range = False
                if campvisum.start_date and campvisum.start_date >= start_date:
                    date_in_range = True
            elif end_date:
                date_in_range = False
                if campvisum.end_date and campvisum.end_date <= end_date:
                    date_in_range = True

            if date_in_range:
                location = campvisum.location
                if location:
                    location["camp"] = CampMinimalSerializer(
                        campvisum, many=False
                    ).data
                    location["camp"]["group"] = ScoutsGroupSerializer(
                        group, many=False
                    ).data
                    locations.append(location)
        return Response(locations)
