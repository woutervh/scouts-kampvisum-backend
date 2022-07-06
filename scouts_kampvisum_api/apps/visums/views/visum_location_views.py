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
from scouts_auth.groupadmin.services import ScoutsAuthorizationService

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger
from apps.visums.models import LinkedCategory
from apps.visums.models import LinkedSubCategory
from apps.visums.models import LinkedLocationCheck

logger: InuitsLogger = logging.getLogger(__name__)


class CampVisumLocationViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing and editing camp instances.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CampLocationMinimalSerializer
    queryset = CampVisum.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CampVisumFilter

    camp_visum_service = CampVisumService()
    authorization_service = ScoutsAuthorizationService()

    def get_permissions(self):
        current_permissions = super().get_permissions()

        if self.action == "retrieve":
            current_permissions.append(CustomDjangoPermission("visums.view_visum"))
        if self.action == "create":
            current_permissions.append(CustomDjangoPermission("visums.edit_visum"))
        if self.action == "update" or self.action == "partial_update":
            current_permissions.append(CustomDjangoPermission("visums.edit_visum"))
        if self.action == "list":
            current_permissions.append(CustomDjangoPermission("visums.list_visum"))
            current_permissions.append(CustomDjangoPermission("visums.view_camp_locations"))

        return current_permissions

    @swagger_auto_schema(responses={status.HTTP_200_OK: CampLocationMinimalSerializer})
    def list(self, request):
        # HACKETY HACK
        # This should probably be handled by a rest call when changing groups in the frontend,
        # but adding it here avoids the need for changes to the frontend
        group_admin_id = self.request.query_params.get("group", None)
        # if no group filter then check if user is in X1027G to show all locations
        if group_admin_id is None:
            group_admin_id = "X1027G"
        scouts_group: ScoutsGroup = ScoutsGroup.objects.safe_get(
            group_admin_id=group_admin_id, raise_error=True
        )
        self.authorization_service.update_user_authorizations(
            user=request.user, scouts_group=scouts_group
        )

        campvisums = self.filter_queryset(self.get_queryset())
        locations = list()
        for campvisum in campvisums:
            linked_categories = LinkedCategory.objects.filter(category_set__id=campvisum.category_set.id,
                                                              parent__name="logistics")
            for linked_category in linked_categories:
                linked_sub_categories = LinkedSubCategory.objects.filter(category=linked_category.id,
                                                                         parent__name="logistics_locations")
                for linked_sub_category in linked_sub_categories:
                    linked_checks = LinkedLocationCheck.objects.filter(sub_category=linked_sub_category.id,
                                                                       parent__name="logistics_locations_location")
                    for linked_check in linked_checks:
                        for linked_location in linked_check.locations.all():
                            for camp_location in CampLocation.objects.filter(location_id=linked_location.id):
                                location = CampLocationMinimalSerializer(
                                    camp_location, many=False
                                ).data
                                location["visum_id"] = campvisum.id
                                location["name"] = linked_location.name
                                location["camp"] = CampMinimalSerializer(campvisum.camp, many=False).data
                                location["camp"]["group"] = ScoutsGroupSerializer(campvisum.group, many=False).data
                                locations.append(location)

        return Response(locations)
