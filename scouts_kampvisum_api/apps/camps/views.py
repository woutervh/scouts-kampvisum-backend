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
from .serializers import CampSerializer
from .filters import CampFilter


logger = logging.getLogger(__name__)


class CampViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing and editing camp instances.
    """
    
    lookup_field = 'pk'
    serializer_class = CampSerializer
    queryset = Camp.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CampFilter

    @swagger_auto_schema(
        request_body=CampSerializer,
        responses={status.HTTP_201_CREATED: CampSerializer},
    )
    def create(self, request):
        data = request.data

        logger.debug("Creating camp with name: '%s'", data.get('name'))

        serializer = CampSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        camp = CampService().camp_create(
            **serializer.validated_data
        )

        output_serializer = CampSerializer(
            camp, context={'request': request}
        )

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CampSerializer})
    def retrieve(self, request, pk=None):
        camp = self.get_object()
        serializer = CampSerializer(
            camp, context={'request': request}
        )

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CampSerializer,
        responses={status.HTTP_200_OK: CampSerializer},
    )
    def partial_update(self, request, pk=None):
        camp = self.get_object()

        serializer = CampSerializer(
            data=request.data,
            instance=camp,
            context={'request': request},
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        logger.debug("Updating Camp with pk %s", pk)

        updated_camp = CampService().camp_update(
            camp=camp, **serializer.validated_data
        )

        output_serializer = CampSerializer(
            updated_camp, context={'request': request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: Schema(type=TYPE_STRING)}
    )
    def delete(self, request, pk):
        logger.debug("Deleting Camp with pk %s", pk)

        camp = get_object_or_404(Camp.objects, pk=pk)
        camp.delete()

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CampSerializer})
    def list(self, request):
        instances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = CampSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = CampSerializer(instances, many=True)
            return Response(serializer.data)

    @action(
        detail=True, methods=['get'], permission_classes=[IsAuthenticated],
        url_path='years')
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: CampSerializer}
    )
    def get_available_years(self, request, pk=None):
        camps = Camp.objects.filter(
            sections__group__id=pk).distinct()
        years = list(set([camp.start_date.year for camp in camps]))

        return Response(years)
