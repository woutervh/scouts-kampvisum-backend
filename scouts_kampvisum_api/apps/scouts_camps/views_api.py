import logging
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from django_filters import rest_framework as filters
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.openapi import Schema, TYPE_STRING

from .models import ScoutsCamp
from .services import ScoutsCampService
from .serializers import ScoutsCampSerializer
from .filters import ScoutsCampAPIFilter


logger = logging.getLogger(__name__)


class ScoutsCampAPIViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing and editing camp instances.
    """
    
    lookup_field = 'uuid'
    serializer_class = ScoutsCampSerializer
    queryset = ScoutsCamp.objects.all()
    filter_backends = [ filters.DjangoFilterBackend ]
    filterset_class = ScoutsCampAPIFilter
    
    @swagger_auto_schema(
        request_body=ScoutsCampSerializer,
        responses={status.HTTP_201_CREATED: ScoutsCampSerializer},
    )
    def create(self, request):
        data = request.data

        logger.debug("Creating camp with name: '%s'", data.get('name'))

        serializer = ScoutsCampSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        camp = ScoutsCampService().camp_create(
            **serializer.validated_data
        )

        output_serializer = ScoutsCampSerializer(
            camp, context={'request': request}
        )

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: ScoutsCampSerializer}
    )
    def retrieve(self, request, uuid=None):
        camp = self.get_object()
        serializer = ScoutsCampSerializer(
            camp, context={'request': request}
        )

        return Response(serializer.data)
    
    @swagger_auto_schema(
        request_body=ScoutsCampSerializer,
        responses={status.HTTP_200_OK: ScoutsCampSerializer},
    )
    def partial_update(self, request, uuid=None):
        camp = self.get_object()

        serializer = ScoutsCampSerializer(
            data=request.data,
            instance=camp,
            context={'request': request},
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        updated_camp = ScoutsCampService().camp_update(
            camp=camp, **serializer.validated_data
        )

        output_serializer = ScoutsCampSerializer(
            updated_camp, context={'request': request}
        )
        
        return Response(output_serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: Schema(type=TYPE_STRING)}
    )
    def delete(self, request, uuid):
        logger.debug("Deleting ScoutsCamp with uuid %s", uuid)
        
        camp = get_object_or_404(ScoutsCamp.objects, uuid=uuid)
        camp.delete()
        
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsCampSerializer})
    def list(self, request):
        instances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = ScoutsCampSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = ScoutsCampSerializer(instances, many=True)
            return Response(serializer.data)

