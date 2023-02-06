from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.openapi import Schema, TYPE_STRING

from apps.camps.models import CampYear
from apps.camps.serializers import CampYearSerializer
from apps.camps.services import CampYearService

from scouts_auth.scouts.permissions import ScoutsFunctionPermissions


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampYearViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing and editing camp year instances.
    """

    serializer_class = CampYearSerializer
    queryset = CampYear.objects.all()
    permission_classes = (ScoutsFunctionPermissions, )
    filter_backends = [filters.DjangoFilterBackend]

    camp_year_service = CampYearService()

    @swagger_auto_schema(
        request_body=CampYearSerializer,
        responses={status.HTTP_201_CREATED: CampYearSerializer},
    )
    def create(self, request):
        # logger.debug("CAMP YEAR CREATE REQUEST DATA: %s", request.data)

        serializer = CampYearSerializer(
            data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        # logger.debug("CAMP YEAR CREATE VALIDATED DATA: %s", validated_data)

        camp = self.camp_year_service.create_year(request, **validated_data)

        output_serializer = CampYearSerializer(
            camp, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CampYearSerializer})
    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = CampYearSerializer(instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CampYearSerializer,
        responses={status.HTTP_200_OK: CampYearSerializer},
    )
    def partial_update(self, request, pk=None):
        camp = self.get_object()

        serializer = CampYearSerializer(
            data=request.data, instance=camp, context={"request": request}, partial=True
        )
        serializer.is_valid(raise_exception=True)

        # logger.debug("Updating CampYear with id %s", pk)

        updated_camp = self.camp_year_service.camp_update(
            request, instance=camp, **serializer.validated_data
        )

        output_serializer = CampYearSerializer(
            updated_camp, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: Schema(type=TYPE_STRING)}
    )
    def delete(self, request, pk):
        # logger.debug("Deleting CampYear with id %s", pk)

        camp = get_object_or_404(CampYear.objects, pk=pk)
        camp.delete()

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CampYearSerializer})
    def list(self, request):
        instances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = CampYearSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = CampYearSerializer(instances, many=True)
            return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path=r"year/(?P<year>\w+)",
    )
    @swagger_auto_schema(responses={status.HTTP_200_OK: CampYearSerializer})
    def retrieve_by_year(self, request, year):
        instance: CampYear = CampYear.objects.get(year=year)
        serializer = CampYearSerializer(instance, context={"request": request})

        return Response(serializer.data)
