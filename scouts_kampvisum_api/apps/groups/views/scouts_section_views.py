import logging
from typing import List

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema

from apps.groups.models import ScoutsSection
from apps.groups.serializers import ScoutsSectionSerializer


logger = logging.getLogger(__name__)


class ScoutsSectionViewSet(viewsets.GenericViewSet):

    serializer_class = ScoutsSectionSerializer
    queryset = ScoutsSection.objects.all()

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
