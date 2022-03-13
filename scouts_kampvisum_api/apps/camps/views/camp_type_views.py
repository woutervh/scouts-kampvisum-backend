from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.openapi import Schema, TYPE_STRING

from apps.camps.models import CampType
from apps.camps.services import CampTypeService
from apps.camps.serializers import CampTypeSerializer
from apps.camps.filters import CampTypeFilter


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampTypeViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing and editing CampType instances.
    """

    serializer_class = CampTypeSerializer
    filterset_class = CampTypeFilter
    queryset = CampType.objects.all().selectable()

    camp_type_service = CampTypeService()

    @swagger_auto_schema(
        request_body=CampTypeSerializer,
        responses={status.HTTP_201_CREATED: CampTypeSerializer},
    )
    def create(self, request):
        """
        Creates a new CampType instance.
        """
        # logger.debug("CAMP TYPE CREATE REQUEST DATA: %s", request.data)
        input_serializer = CampTypeSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        # logger.debug("CAMP TYPE CREATE VALIDATED DATA: %s", validated_data)

        instance = self.camp_type_service.create(request, **validated_data)

        output_serializer = CampTypeSerializer(instance, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CampTypeSerializer})
    def retrieve(self, request, pk=None):
        """
        Gets and returns a CampType instance from the db.
        """

        instance = self.get_object()
        serializer = CampTypeSerializer(instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CampTypeSerializer,
        responses={status.HTTP_200_OK: CampTypeSerializer},
    )
    def partial_update(self, request, pk=None):
        """
        Updates a CampType instance.
        """

        instance = self.get_object()

        # logger.debug("CAMP TYPE UPDATE REQUEST DATA: %s", request.data)
        serializer = CampTypeSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        # logger.debug("CAMP TYPE UPDATE VALIDATED DATA: %s", validated_data)

        updated_instance = self.camp_type_service.update(
            request, instance=instance, **validated_data
        )

        output_serializer = CampTypeSerializer(
            updated_instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: Schema(type=TYPE_STRING)}
    )
    def delete(self, request, pk):
        """
        Deletes a CampType instance.
        """

        instance = get_object_or_404(CampType.objects, pk=pk)
        instance.delete()

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CampTypeSerializer})
    def list(self, request):
        """
        Gets all CampType instances (filtered).
        """

        instances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = CampTypeSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = CampTypeSerializer(instances, many=True)
            return Response(serializer.data)
