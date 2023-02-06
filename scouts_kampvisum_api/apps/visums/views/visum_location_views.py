from datetime import datetime

from django.http.response import HttpResponse
from django_filters import rest_framework as filters
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.openapi import Schema, TYPE_STRING

from apps.visums.models import CampVisum
from apps.visums.serializers import CampVisumSerializer
from apps.visums.filters import CampVisumFilter
from apps.visums.services import CampVisumService
from apps.locations.models import CampLocation
from apps.locations.serializers import CampLocationMinimalSerializer
from apps.camps.serializers import CampMinimalSerializer

from scouts_auth.auth.permissions import CustomDjangoPermission
from scouts_auth.groupadmin.models import ScoutsGroup
from scouts_auth.groupadmin.serializers import ScoutsGroupSerializer
from scouts_auth.groupadmin.settings import GroupAdminSettings
from scouts_auth.scouts.services import ScoutsPermissionService
from scouts_auth.scouts.permissions import ScoutsFunctionPermissions

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger
from apps.visums.models import LinkedCategory
from apps.visums.models import LinkedSubCategory
from apps.visums.models import LinkedLocationCheck
from apps.visums.models import LinkedDurationCheck

logger: InuitsLogger = logging.getLogger(__name__)


class CampVisumLocationViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing and editing camp instances.
    """

    serializer_class = CampLocationMinimalSerializer
    queryset = CampVisum.objects.all()
    permission_classes = (ScoutsFunctionPermissions, )
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CampVisumFilter

    camp_visum_service = CampVisumService()

    @swagger_auto_schema(responses={status.HTTP_200_OK: CampLocationMinimalSerializer})
    def list(self, request):
        # HACKETY HACK
        # This should probably be handled by a rest call when changing groups in the frontend,
        # but adding it here avoids the need for changes to the frontend
        group_admin_id = self.request.query_params.get("group", None)
        # if no group filter then check if user is in X1027G to show all locations
        if group_admin_id is None and not request.user.has_role_administrator():
            raise PermissionDenied("You have to be an admin to make this call")

        campvisums = self.filter_queryset(self.get_queryset())
        locations = list()
        in_range = True
        for campvisum in campvisums:
            if request.query_params.get("start_date") and request.query_params.get("end_date"):
                in_range = False
                plannings = LinkedCategory.objects.filter(category_set__id=campvisum.category_set.id,
                                                          parent__name="planning")
                for planning in plannings:
                    linked_sub_categories_planning_date = LinkedSubCategory.objects.filter(
                        category=planning.id,
                        parent__name="planning_date")
                    for linked_planning_date in linked_sub_categories_planning_date:
                        logger.debug(linked_planning_date)
                        linked_planning_date_leaders_checks = LinkedDurationCheck.objects.filter(
                            sub_category=linked_planning_date.id,
                            parent__name="planning_date_leaders")
                        for linked_planning_date_leaders_check in linked_planning_date_leaders_checks:
                            if linked_planning_date_leaders_check.start_date and linked_planning_date_leaders_check.end_date and (linked_planning_date_leaders_check.start_date <= datetime.strptime(request.query_params.get(
                                    "end_date"), '%Y-%m-%d').date() and linked_planning_date_leaders_check.end_date >= datetime.strptime(request.query_params.get(
                                    "start_date"), '%Y-%m-%d').date()):
                                in_range = True
            if in_range:
                logistics = LinkedCategory.objects.filter(category_set__id=campvisum.category_set.id,
                                                          parent__name="logistics")
                for linked_category in logistics:

                    linked_sub_categories_logistics_locations = LinkedSubCategory.objects.filter(
                        category=linked_category.id,
                        parent__name="logistics_locations")
                    for linked_sub_category in linked_sub_categories_logistics_locations:
                        linked_location_checks = LinkedLocationCheck.objects.filter(sub_category=linked_sub_category.id,
                                                                                    parent__name="logistics_locations_location")
                        for linked_location_check in linked_location_checks:
                            for linked_location in linked_location_check.locations.all():
                                for camp_location in CampLocation.objects.filter(location_id=linked_location.id):
                                    location = CampLocationMinimalSerializer(
                                        camp_location, many=False
                                    ).data
                                    location["visum_id"] = campvisum.id
                                    location["name"] = linked_location.name
                                    location["start_date"] = linked_location.start_date
                                    location["end_date"] = linked_location.end_date
                                    location["camp"] = CampMinimalSerializer(
                                        campvisum.camp, many=False).data
                                    location["camp"]["group"] = ScoutsGroupSerializer(
                                        campvisum.group, many=False).data
                                    locations.append(location)

        return Response(locations)
