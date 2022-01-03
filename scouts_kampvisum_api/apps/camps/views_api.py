import logging

from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.openapi import Schema, TYPE_STRING

from .models import Camp
from .services import CampService
from .serializers import CampSerializer, CampAPISerializer
from .filters import CampAPIFilter

logger = logging.getLogger(__name__)


class CampAPIViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing and editing camp instances.
    """

    serializer_class = CampSerializer
    queryset = Camp.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CampAPIFilter

    camp_service = CampService()

    @swagger_auto_schema(
        request_body=CampAPISerializer,
        responses={status.HTTP_201_CREATED: CampSerializer},
    )
    def create(self, request):
        logger.debug("CREATE REQUEST DATA: %s", request.data)

        serializer = CampAPISerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("CREATE VALIDATED DATA: %s", validated_data)

        camp = self.camp_service.camp_create(**validated_data)

        output_serializer = CampSerializer(camp, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CampAPISerializer})
    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = CampAPISerializer(instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CampAPISerializer,
        responses={status.HTTP_200_OK: CampSerializer},
    )
    def partial_update(self, request, pk=None):
        camp = self.get_object()

        serializer = CampAPISerializer(
            data=request.data, instance=camp, context={"request": request}, partial=True
        )
        serializer.is_valid(raise_exception=True)

        logger.debug("Updating Camp with id %s", pk)

        updated_camp = CampService().camp_update(
            instance=camp, **serializer.validated_data
        )

        output_serializer = CampSerializer(updated_camp, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: Schema(type=TYPE_STRING)}
    )
    def delete(self, request, pk):
        logger.debug("Deleting Camp with id %s", pk)

        camp = get_object_or_404(Camp.objects, pk=pk)
        camp.delete()

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CampAPISerializer})
    def list(self, request):
        instances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = CampAPISerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = CampAPISerializer(instances, many=True)
            return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path=r"(?P<group_admin_id>\w+)/years",
    )
    @swagger_auto_schema(responses={status.HTTP_200_OK: CampSerializer})
    def get_available_years(self, request, group_admin_id=None):
        camps = Camp.objects.filter(sections__group_admin_id=group_admin_id).distinct()

        if camps.count() != 0:
            years = list(
                set(
                    [
                        camp.start_date.year
                        for camp in camps
                        if camp.start_date is not None
                    ]
                )
            )
            return Response(years)

        return Response(list())
