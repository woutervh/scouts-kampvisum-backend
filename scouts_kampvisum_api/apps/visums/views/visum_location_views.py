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

from scouts_auth.auth.permissions import CustomDjangoPermission

from scouts_auth.groupadmin.models import ScoutsGroup
from scouts_auth.groupadmin.services import ScoutsAuthorizationService

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampVisumLocationViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing and editing camp instances.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CampVisumSerializer
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

        return current_permissions

    @swagger_auto_schema(responses={status.HTTP_200_OK: CampVisumSerializer})
    def list(self, request):
        # HACKETY HACK
        # This should probably be handled by a rest call when changing groups in the frontend,
        # but adding it here avoids the need for changes to the frontend
        group_admin_id = self.request.query_params.get("group", None)
        scouts_group: ScoutsGroup = ScoutsGroup.objects.safe_get(
            group_admin_id=group_admin_id, raise_error=True
        )
        self.authorization_service.update_user_authorizations(
            user=request.user, scouts_group=scouts_group
        )

        instances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(instances)

        serializer = CampVisumSerializer(
            page, many=True, context={"request": request}
        ) if page is not None else CampVisumSerializer(
            instances, many=True, context={"request": request}
        )

        ordered = sorted(serializer.data,
                         key=lambda k: k.get("camp", {}).get("sections", [{"age_group": 0}])[0].get("age_group", 0)
                         if len(k.get("camp", {}).get("sections", [{"age_group": 0}])) > 0 else 0)
        i = 0
        for camp in ordered:
            for category in camp.get("category_set").get("categories"):
                if category.get('parent').get('name') == "logistics":
                    for sub_category in category.get("sub_categories"):
                        if sub_category.get("parent").get("name") == "logistics_locations":
                            for check in sub_category.get("checks"):
                                if check.get("parent").get("name") == "logistics_locations_location":
                                    ordered[i] = check.get("value")
            i = i + 1

        return self.get_paginated_response(ordered) if page is not None else Response(ordered)
