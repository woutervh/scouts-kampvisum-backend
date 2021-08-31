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

from ..models import CampVisum
from ..serializers import CampVisumSerializer
from ..filters import CampVisumFilter, CampVisumAPIFilter
from ..services import CampVisumService


logger = logging.getLogger(__name__)


class CampVisumAPIViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing and editing camp instances.
    """

    lookup_field = 'uuid'
    serializer_class = CampVisumSerializer
    queryset = CampVisum.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CampVisumAPIFilter

    @swagger_auto_schema(
        request_body=CampVisumSerializer,
        responses={status.HTTP_201_CREATED: CampVisumSerializer},
    )
    def create(self, request):
        data = request.data

        logger.debug("DATA: %s", data)
        serializer = CampVisumSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        logger.debug("VALIDATED DATA: %s", serializer.validated_data)

        camp = CampVisumService().visum_create(
            **serializer.validated_data
        )

        output_serializer = CampVisumSerializer(
            camp, context={'request': request}
        )

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CampVisumSerializer})
    def list(self, request):
        instances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = CampVisumSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = CampVisumSerializer(instances, many=True)
            return Response(serializer.data)

    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: Schema(type=TYPE_STRING)}
    )
    def destroy(self, request, uuid):
        logger.debug("Deleting CampVisum with uuid %s", uuid)

        instance = get_object_or_404(CampVisum.objects, uuid=uuid)
        instance.delete()

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
