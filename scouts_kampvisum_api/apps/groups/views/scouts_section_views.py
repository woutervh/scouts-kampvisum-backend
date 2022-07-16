from typing import List

from django.http.response import HttpResponse
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.openapi import Schema, TYPE_STRING

from apps.groups.models import ScoutsSection
from apps.groups.serializers import ScoutsSectionSerializer
from apps.groups.services import ScoutsSectionService

from scouts_auth.auth.permissions import CustomDjangoPermission

from scouts_auth.groupadmin.models import ScoutsGroup
from scouts_auth.groupadmin.services import ScoutsAuthorizationService


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsSectionViewSet(viewsets.GenericViewSet):

    serializer_class = ScoutsSectionSerializer
    queryset = ScoutsSection.objects.all().filter(hidden=False)

    section_service = ScoutsSectionService()
    authorization_service = ScoutsAuthorizationService()

    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        current_permissions = super().get_permissions()

        if self.action == "retrieve":
            current_permissions.append(CustomDjangoPermission("groups.view_section"))
        elif self.action == "create":
            current_permissions.append(CustomDjangoPermission("groups.edit_section"))
        elif self.action == "update" or self.action == "partial_update":
            current_permissions.append(CustomDjangoPermission("groups.edit_section"))
        elif self.action == "list":
            current_permissions.append(CustomDjangoPermission("groups.list_section"))
        elif self.action == "destroy":
            current_permissions.append(CustomDjangoPermission("groups.delete_section"))

        return current_permissions

    @swagger_auto_schema(
        request_body=ScoutsSectionSerializer,
        responses={status.HTTP_201_CREATED: ScoutsSectionSerializer},
    )
    def create(self, request):
        """
        Creates a new ScoutSection.
        """
        logger.debug("SECTION CREATE REQUEST DATA: %s", request.data)
        input_serializer = ScoutsSectionSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("SECTION CREATE VALIDATED DATA: %s", validated_data)

        instance = self.section_service.section_create_or_update(
            request, section=validated_data
        )

        output_serializer = ScoutsSectionSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsSectionSerializer})
    def retrieve(self, request, pk=None):
        """
        Retrieves an existing ScoutSectionName object.
        """
        instance: ScoutsSection = self.get_object()
        serializer = ScoutsSectionSerializer(instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ScoutsSectionSerializer,
        responses={status.HTTP_200_OK: ScoutsSectionSerializer},
    )
    def partial_update(self, request, pk=None):
        """
        Updates an existing ScoutsSection object.
        """
        instance = ScoutsSection.objects.safe_get(pk=pk, raise_error=True)

        serializer = ScoutsSectionSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        updated_instance = self.section_service.section_create_or_update(
            request, instance=instance, section=serializer.validated_data
        )

        output_serializer = ScoutsSectionSerializer(
            updated_instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: Schema(type=TYPE_STRING)}
    )
    def delete(self, request, pk=None):
        """
        Deletes a ScoutsSection instance by uuid
        """
        instance = ScoutsSection.objects.get(pk=pk)

        if not instance:
            logger.error("No Section found with id '%s'", pk)
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        instance.delete()

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsSectionSerializer})
    def list(self, request):
        """
        Retrieves a list of all existing Section instances.
        """

        instances: List[ScoutsSection] = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = ScoutsSectionSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)
        else:
            serializer = ScoutsSectionSerializer(
                instances, many=True, context={"request": request}
            )
            return Response(serializer.data)

    # @TODO in filter
    @action(
        detail=False,
        methods=["get"],
        url_path=r"(?P<group_admin_id>\w+)",
    )
    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsSectionSerializer})
    def list_by_group(self, request, group_admin_id):
        group: ScoutsGroup = ScoutsGroup.objects.safe_get(
            group_admin_id=group_admin_id, raise_error=True
        )

        # HACKETY HACK
        # This should probably be handled by a rest call when changing groups in the frontend,
        # but adding it here avoids the need for changes to the frontend
        self.authorization_service.update_user_authorizations(
            user=request.user, scouts_group=group
        )
        instances = ScoutsSection.objects.all().filter(
            group__group_admin_id=group_admin_id, hidden=False
        )
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = ScoutsSectionSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)
        else:
            serializer = ScoutsSectionSerializer(
                instances, many=True, context={"request": request}
            )
            return Response(serializer.data)
