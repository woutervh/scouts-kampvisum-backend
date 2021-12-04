import logging

from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from apps.groups.models import ScoutsSection
from apps.groups.serializers import ScoutsSectionSerializer


logger = logging.getLogger(__name__)


class ScoutsSectionViewSet(viewsets.GenericViewSet):

    lookup_field = "uuid"
    serializer_class = ScoutsSectionSerializer
    queryset = ScoutsSection.objects.all()

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsSectionSerializer})
    def retrieve(self, request, uuid=None):
        """
        Retrieves an existing ScoutSectionName object.
        """
        instance = self.get_object()
        serializer = ScoutsSectionSerializer(instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsSectionSerializer})
    def list(self, request):
        """
        Retrieves a list of all existing Section instances.
        """

        instances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = ScoutsSectionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = ScoutsSectionSerializer(instances, many=True)
            return Response(serializer.data)
