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


class CampVisumViewSet(viewsets.GenericViewSet):
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

    def check_user_allowed(self, request, group):
        # This should probably be handled by a rest call when changing groups in the frontend,
        # but adding it here avoids the need for changes to the frontend
        self.authorization_service.update_user_authorizations(
            user=request.user, scouts_group=group
        )
        logger.debug("Updated user authorisations with group %s",
                     group.group_admin_id, user=request.user)

    def get_permissions(self):
        current_permissions = super().get_permissions()

        if self.action == "retrieve":
            current_permissions.append(
                CustomDjangoPermission("visums.view_visum"))
        elif self.action == "create":
            current_permissions.append(
                CustomDjangoPermission("visums.edit_visum"))
        elif self.action == "update" or self.action == "partial_update":
            current_permissions.append(
                CustomDjangoPermission("visums.edit_visum"))
        elif self.action == "list":
            current_permissions.append(
                CustomDjangoPermission("visums.list_visum"))
        elif self.action == "destroy":
            current_permissions.append(
                CustomDjangoPermission("visums.delete_visum"))

        return current_permissions

    @swagger_auto_schema(
        request_body=CampVisumSerializer,
        responses={status.HTTP_201_CREATED: CampVisumSerializer},
    )
    def create(self, request):
        data = request.data

        logger.debug("CAMP VISUM CREATE REQUEST DATA: %s", data)
        serializer = CampVisumSerializer(
            data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("CAMP VISUM CREATE VALIDATED DATA: %s", validated_data)

        group = validated_data.get("group", None)
        scouts_group = ScoutsGroup.objects.safe_get(group_admin_id=group)
        if (
            not group
            or not group
            in [
                group.group_admin_id
                for group in request.user.persisted_scouts_groups.all()
            ]
            or not scouts_group
            or (not request.user.has_role_leader(group=scouts_group))
            and (not request.user.has_role_district_commissioner(group=scouts_group))
        ):
            raise PermissionDenied(
                {
                    "message": "You don't have permission to create camps for group {}".format(
                        group
                    )
                }
            )

        visum: CampVisum = self.camp_visum_service.visum_create(
            request, **validated_data
        )

        output_serializer = CampVisumSerializer(
            visum, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CampVisumSerializer})
    def retrieve(self, request, pk=None):
        logger.debug(f"Requesting visum {pk}", user=request.user)
        instance = self.get_object()
        logger.debug(f"Visum retrieved: {instance.camp.name}")
        # HACKETY HACK
        # This should probably be handled by a rest call when changing groups in the frontend,
        # but adding it here avoids the need for changes to the frontend
        self.check_user_allowed(request, instance.group)
        logger.debug("Reloaded user permissions")
        serializer = CampVisumSerializer(
            instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CampVisumSerializer,
        responses={status.HTTP_200_OK: CampVisumSerializer},
    )
    def partial_update(self, request, pk=None):
        instance = self.get_object()
        self.check_user_allowed(request, instance.group)

        logger.debug("CAMP VISUM UPDATE REQUEST DATA: %s", request.data)

        serializer = CampVisumSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("CAMP VISUM UPDATE VALIDATED DATA: %s", validated_data)

        logger.debug("Updating CampVisum with id %s", pk)

        updated_instance = self.camp_visum_service.visum_update(
            request, instance=instance, **validated_data
        )

        output_serializer = CampVisumSerializer(
            updated_instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CampVisumSerializer})
    def list(self, request):
        # HACKETY HACK
        # This should probably be handled by a rest call when changing groups in the frontend,
        # but adding it here avoids the need for changes to the frontend
        group_admin_id = self.request.query_params.get("group", None)
        logger.debug("Listing visums for group %s",
                     group_admin_id, user=request.user)
        scouts_group: ScoutsGroup = ScoutsGroup.objects.safe_get(
            group_admin_id=group_admin_id, raise_error=True
        )
        self.check_user_allowed(request, scouts_group)

        instances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(instances)

        serializer = (
            CampVisumSerializer(page, many=True, context={"request": request})
            if page is not None
            else CampVisumSerializer(instances, many=True, context={"request": request})
        )

        ordered = sorted(
            serializer.data,
            key=lambda k: k.get("camp", {})
            .get("sections", [{"age_group": 0}])[0]
            .get("age_group", 0)
            if len(k.get("camp", {}).get("sections", [{"age_group": 0}])) > 0
            else 0,
        )

        return (
            self.get_paginated_response(ordered)
            if page is not None
            else Response(ordered)
        )

    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: Schema(type=TYPE_STRING)}
    )
    def destroy(self, request, pk):
        instance = CampVisum.objects.safe_get(id=pk)
        self.check_user_allowed(request, instance.group)

        self.camp_visum_service.delete_visum(
            request=request, instance=instance)

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
