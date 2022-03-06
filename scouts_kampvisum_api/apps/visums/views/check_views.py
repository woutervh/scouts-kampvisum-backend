from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.openapi import Schema, TYPE_STRING

from apps.visums.models import Check
from apps.visums.serializers import CheckSerializer
from apps.visums.services import CheckService


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CheckViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing and editing Check instances.
    """

    serializer_class = CheckSerializer
    queryset = Check.objects.all()

    check_service = CheckService()

    @swagger_auto_schema(
        request_body=CheckSerializer,
        responses={status.HTTP_201_CREATED: CheckSerializer},
    )
    def create(self, request):
        """
        Creates a new check instance.
        """
        logger.debug("CHECK CREATE REQUEST DATA: %s", request.data)
        input_serializer = CheckSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("CHECK CREATE VALIDATED DATA: %s", validated_data)

        instance = self.check_service.camp_create(request, **validated_data)

        output_serializer = CheckSerializer(instance, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CheckSerializer})
    def retrieve(self, request, pk=None):
        """
        Gets and returns a check instance from the db.
        """

        instance = self.get_object()
        serializer = CheckSerializer(instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CheckSerializer,
        responses={status.HTTP_200_OK: CheckSerializer},
    )
    def partial_update(self, request, pk=None):
        """
        Updates a check instance.
        """

        instance = self.get_object()

        logger.debug("CHECK UPDATE REQUEST DATA: %s", request.data)
        serializer = CheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("CHECK UPDATE VALIDATED DATA: %s", validated_data)

        updated_instance = self.check_service.update(
            request, instance=instance, **validated_data
        )

        output_serializer = CheckSerializer(
            updated_instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: Schema(type=TYPE_STRING)}
    )
    def delete(self, request, pk):
        """
        Deletes a check instance.
        """

        instance = get_object_or_404(Check.objects, pk=pk)
        instance.delete()

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CheckSerializer})
    def list(self, request):
        """
        Gets all check instances (filtered).
        """

        instances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = CheckSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = CheckSerializer(instances, many=True)
            return Response(serializer.data)
