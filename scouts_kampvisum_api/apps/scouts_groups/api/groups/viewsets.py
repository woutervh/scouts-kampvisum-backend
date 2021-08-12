from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.openapi import Schema, TYPE_STRING
from scouts_kampvisum_api.apps.scouts_groups.api.sections.models import ScoutsSectionName
from .services import ScoutsSectionNameService
from .serializers import ScoutsSectionNameSerializer


class ScoutsSectionNameViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing and editing scout section names.
    """
    
    serializer_class = ScoutsSectionNameSerializer
    queryset = ScoutsSectionName.objects.all()
    
    @swagger_auto_schema(
        request_body=ScoutsSectionNameSerializer,
        responses={status.HTTP_201_CREATED: ScoutsSectionNameSerializer},
    )
    def create(self, request):
        """
        Creates a new ScoutSectionName.
        """
        
        input_serializer = ScoutsSectionNameSerializer(
            data=request.data, context={'request': request}
        )
        input_serializer.is_valid(raise_exception=True)

        instance = ScoutsSectionNameService().name_create(
            **input_serializer.validated_data
        )

        output_serializer = ScoutsSectionNameSerializer(
            instance, context={'request': request}
        )

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: ScoutsSectionNameSerializer}
    )
    def retrieve(self, request, pk=None):
        """
        Retrieves an existing ScoutSectionName object.
        """
        
        instance = self.get_object()
        serializer = ScoutsSectionNameSerializer(
            instance, context={'request': request}
        )

        return Response(serializer.data)
    
    @swagger_auto_schema(
        request_body=ScoutsSectionNameSerializer,
        responses={status.HTTP_200_OK: ScoutsSectionNameSerializer},
    )
    def partial_update(self, request, pk=None):
        """
        Updates an existing ScoutsSectionName object.
        """
        
        instance = self.get_object()

        serializer = ScoutsSectionNameSerializer(
            data=request.data,
            instance=instance,
            context={'request': request},
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        updated_instance = ScoutsSectionNameService().name_update(
            instance=instance, **serializer.validated_data
        )

        output_serializer = ScoutsSectionNameSerializer(
            updated_instance, context={'request': request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: Schema(type=TYPE_STRING)}
    )
    def delete(self, request, pk):
        """
        Deletes a ScoutsSectionName instance.
        """
        
        instance = get_object_or_404(ScoutsSectionName.objects, pk=pk)
        instance.delete()
        
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: ScoutsSectionNameSerializer}
    )
    def list(self, request):
        """
        Retrieves a list of all existing ScoutsSectionName instances.
        """
        
        instances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = ScoutsSectionNameSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = ScoutsSectionNameSerializer(instances, many=True)
            return Response(serializer.data)

