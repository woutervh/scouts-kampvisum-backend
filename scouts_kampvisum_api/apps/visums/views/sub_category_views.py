from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.openapi import Schema, TYPE_STRING

from apps.visums.models import SubCategory
from apps.visums.services import SubCategoryService
from apps.visums.serializers import SubCategorySerializer

from scouts_auth.scouts.permissions import ScoutsFunctionPermissions


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class SubCategoryViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing and editing SubCategory instances.
    """

    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()
    permission_classes = (ScoutsFunctionPermissions, )

    sub_category_service = SubCategoryService()

    @swagger_auto_schema(
        request_body=SubCategorySerializer,
        responses={status.HTTP_201_CREATED: SubCategorySerializer},
    )
    def create(self, request):
        """
        Creates a new SubCategory instance.
        """
        logger.debug("SUB CATEGORY CREATE REQUEST DATA: %s", request.data)
        input_serializer = SubCategorySerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("SUB CATEGORY CREATE VALIDATED DATA: %s", validated_data)

        instance = self.sub_category_service.camp_create(
            request, **validated_data)

        output_serializer = SubCategorySerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: SubCategorySerializer})
    def retrieve(self, request, pk=None):
        """
        Gets and returns a SubCategory instance from the db.
        """

        instance = self.get_object()
        serializer = SubCategorySerializer(
            instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=SubCategorySerializer,
        responses={status.HTTP_200_OK: SubCategorySerializer},
    )
    def partial_update(self, request, pk=None):
        """
        Updates a SubCategory instance.
        """

        instance = self.get_object()

        logger.debug("SUB CATEGORY UPDATE REQUEST DATA: %s", request.data)
        serializer = SubCategorySerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("SUB CATEGORY UPDATE VALIDATED DATA: %s", validated_data)

        updated_instance = self.sub_category_service.update(
            request, instance=instance, **validated_data
        )

        output_serializer = SubCategorySerializer(
            updated_instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: Schema(type=TYPE_STRING)}
    )
    def delete(self, request, pk):
        """
        Deletes a SubCategory instance.
        """

        instance = get_object_or_404(SubCategory.objects, pk=pk)
        instance.delete()

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={status.HTTP_200_OK: SubCategorySerializer})
    def list(self, request):
        """
        Gets all SubCategory instances (filtered).
        """

        instances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = SubCategorySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = SubCategorySerializer(instances, many=True)
            return Response(serializer.data)
