from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.openapi import Schema, TYPE_STRING

from .models import ScoutsCamp
from .services import ScoutsCampService
from .serializers import ScoutsCampSerializer, ScoutsCampDeserializer


class ScoutsCampViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing and editing camp instances.
    """
    
    serializer_class = ScoutsCampSerializer
    queryset = ScoutsCamp.objects.all()
    
    @swagger_auto_schema(
        request_body=ScoutsCampDeserializer,
        responses={status.HTTP_201_CREATED: ScoutsCampSerializer},
    )
    def create(self, request):
        input_serializer = ScoutsCampDeserializer(
            data=request.data, context={'request': request}
        )
        input_serializer.is_valid(raise_exception=True)

        camp = ScoutsCampService().camp_create(
            **input_serializer.validated_data
        )

        output_serializer = ScoutsCampSerializer(
            camp, context={'request': request}
        )

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsCampSerializer})
    def retrieve(self, request, pk=None):
        camp = self.get_object()
        serializer = ScoutsCampSerializer(
            camp, context={'request': request}
        )

        return Response(serializer.data)
    
    @swagger_auto_schema(
        request_body=ScoutsCampDeserializer,
        responses={status.HTTP_200_OK: ScoutsCampSerializer},
    )
    def partial_update(self, request, pk=None):
        camp = self.get_object()

        serializer = ScoutsCampDeserializer(
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
    def delete(self, request, pk):
        camp = get_object_or_404(ScoutsCamp.objects, pk=pk)
        camp.delete()
        
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsCampSerializer})
    def list(self, request):
        equipment = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(equipment)

        if page is not None:
            serializer = ScoutsCampSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = ScoutsCampSerializer(equipment, many=True)
            return Response(serializer.data)

