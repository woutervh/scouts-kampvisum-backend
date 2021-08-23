import logging
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from django_filters import rest_framework as filters
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.openapi import Schema, TYPE_STRING

from .models import ScoutsCamp
from .services import ScoutsCampService
from .serializers import ScoutsCampSerializer
from .serializers_api import ScoutsCampAPISerializer
from .filters import ScoutsCampAPIFilter
from apps.scouts_groups.api.models import ScoutsGroup

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
        request_body=ScoutsCampAPISerializer,
        responses={status.HTTP_201_CREATED: ScoutsCampSerializer},
    )
    def create(self, request):
        data = request.data

        logger.debug("Creating camp with name: '%s'", data.get('name'))

        logger.info("SECTIONS: %s", data.get('sections'))
        serializer = ScoutsCampAPISerializer(
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

        logger.debug("Updating ScoutsCamp with uuid %s", uuid)

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
    
    @action(
        detail=True, methods=['get'], permission_classes=[IsAuthenticated],
        url_path='years')
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: ScoutsCampSerializer}
    )
    def get_available_years(self, request, uuid=None):
        camps = ScoutsCamp.objects.filter(
            sections__group__uuid=uuid).distinct()
        years = list(set([ camp.start_date.year for camp in camps ]))

        return Response(years)

        

