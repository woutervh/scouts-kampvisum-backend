import logging

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.openapi import Schema, TYPE_STRING

from scouts_auth.inuits.models import PersistedFile
from scouts_auth.inuits.filters import PersistedFileFilter
from scouts_auth.inuits.services import PersistedFileService
from scouts_auth.inuits.serializers import PersistedFileSerializer


logger = logging.getLogger(__name__)


class PersistedFileViewSet(viewsets.GenericViewSet):

    """
    A viewset for viewing and editing PersistedFile instances.
    """

    serializer_class = PersistedFileSerializer
    queryset = PersistedFile.objects.all()
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = PersistedFileFilter

    persisted_file_service = PersistedFileService()

    @swagger_auto_schema(
        request_body=PersistedFileSerializer,
        responses={status.HTTP_201_CREATED: PersistedFileSerializer},
    )
    def create(self, request):
        """
        Creates a new PersistedFile instance.
        """
        logger.debug("PERSISTED FILE CREATE REQUEST DATA: %s", request.data)
        input_serializer = PersistedFileSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("PERSISTED FILE CREATE VALIDATED DATA: %s", validated_data)

        instance = self.persisted_file_service.save(request, **validated_data)

        output_serializer = PersistedFileSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: PersistedFileSerializer})
    def retrieve(self, request, pk=None):
        """
        Gets and returns a PersistedFile instance from the db.
        """

        instance = self.get_object()
        serializer = PersistedFileSerializer(instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=PersistedFileSerializer,
        responses={status.HTTP_200_OK: PersistedFileSerializer},
    )
    def partial_update(self, request, pk=None):
        """
        Updates a PersistedFile instance.
        """

        instance = self.get_object()

        logger.debug("PERSISTED FILE UPDATE REQUEST DATA: %s", request.data)
        serializer = PersistedFileSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("PERSISTED FILE UPDATE VALIDATED DATA: %s", validated_data)

        updated_instance = self.persisted_file_service.update(
            request, instance=instance, **validated_data
        )

        output_serializer = PersistedFileSerializer(
            updated_instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: Schema(type=TYPE_STRING)}
    )
    def delete(self, request, pk):
        """
        Deletes a PersistedFile instance.
        """
        instance: PersistedFile = get_object_or_404(PersistedFile.objects, pk=pk)
        logger.debug(
            "Deleting PersistedFile instance with id %s and name %s",
            instance.id,
            instance.file.name,
        )

        instance.delete()

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={status.HTTP_200_OK: PersistedFileSerializer})
    def list(self, request):
        """
        Gets all PersistedFile instances (filtered).
        """
        instances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = PersistedFileSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = PersistedFileSerializer(instances, many=True)
            return Response(serializer.data)
