import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from apps.locations.models import LinkedLocation
from apps.locations.serializers import LinkedLocationSerializer
from apps.locations.filters import LinkedLocationFilter


logger = logging.getLogger(__name__)


class LocationViewSet(viewsets.GenericViewSet):

    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = LinkedLocationFilter
    ordering_fields = ["id"]
    ordering = ["id"]

    def get_queryset(self):
        return LinkedLocation.objects.all()

    # @swagger_auto_schema(
    #     request_body=CampLocationSerializer,
    #     responses={status.HTTP_201_CREATED: CampLocationSerializer},
    # )
    # def create(self, request):
    #     logger.debug("CAMP LOCATION CREATE REQUEST DATA: %s", request.data)
    #     input_serializer = CampLocationSerializer(
    #         data=request.data, context={"request": request}
    #     )
    #     input_serializer.is_valid(raise_exception=True)

    #     validated_data = input_serializer.validated_data
    #     logger.debug("CAMP LOCATION CREATE VALIDATED REQUEST DATA: %s", validated_data)

    #     instance = self.service.create_or_update(
    #         instance=validated_data, user=request.user
    #     )

    #     output_serializer = CampLocationSerializer(
    #         instance, context={"request": request}
    #     )

    #     return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    # @swagger_auto_schema(responses={status.HTTP_200_OK: CampLocationSerializer})
    # def retrieve(self, request, pk=None):
    #     instance: CampLocation = self.get_object()
    #     serializer = CampLocationSerializer(instance)

    #     return Response(serializer.data)

    # @swagger_auto_schema(
    #     request_body=CampLocationSerializer,
    #     responses={status.HTTP_200_OK: CampLocationSerializer},
    # )
    # def partial_update(self, request, pk=None):
    #     instance = self.get_object()

    #     logger.debug("CAMP LOCATION PARTIAL UPDATE REQUEST DATA: %s", request.data)
    #     serializer = CampLocationSerializer(
    #         instance=instance,
    #         data=request.data,
    #         context={"request": request},
    #         partial=True,
    #     )
    #     serializer.is_valid(raise_exception=True)

    #     validated_data = serializer.validated_data
    #     logger.debug("CAMP LOCATION PARTIAL UPDATE VALIDATED DATA: %s", validated_data)

    #     instance = self.service.update(
    #         instance=instance,
    #         updated_instance=validated_data,
    #         updated_by=request.user,
    #     )

    #     output_serializer = CampLocationSerializer(instance)

    #     return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedLocationSerializer})
    def list(self, request):
        queryset = self.get_queryset()
        instances = self.filter_queryset(queryset)

        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = LinkedLocationSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)
        else:
            serializer = LinkedLocationSerializer(
                instances, many=True, context={"request": request}
            )
            return Response(serializer.data)
