import logging
from typing import List

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema

from apps.groups.models import ScoutsSection
from apps.groups.serializers import ScoutsSectionSerializer
from apps.groups.services import ScoutsSectionService


logger = logging.getLogger(__name__)


class ScoutsSectionViewSet(viewsets.GenericViewSet):

    serializer_class = ScoutsSectionSerializer
    queryset = ScoutsSection.objects.all()

    section_service = ScoutsSectionService()

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
            request, **validated_data
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

    @action(
        detail=False,
        methods=["get"],
        url_path=r"(?P<group_admin_id>\w+)",
    )
    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsSectionSerializer})
    def list_by_group(self, request, group_admin_id):
        instances = ScoutsSection.objects.all().filter(group_admin_id=group_admin_id)
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
