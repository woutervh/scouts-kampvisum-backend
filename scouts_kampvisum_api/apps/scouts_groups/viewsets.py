'''
Created on Jul 27, 2021

@author: boro
'''

from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.openapi import Schema, TYPE_STRING
from .models import ScoutsTroopName
from .services import ScoutsTroopNameService
from .serializers import ScoutsTroopNameSerializer, ScoutsTroopNameDeserializer


class ScoutsTroopNameViewSet(viewsets.GenericViewSet):
    '''
    A viewset for viewing and editing Scout Troop names.
    '''
    
    serializer_class = ScoutsTroopNameSerializer
    queryset = ScoutsTroopName.objects.all()
    
    @swagger_auto_schema(
        request_body=ScoutsTroopNameDeserializer,
        responses={status.HTTP_201_CREATED: ScoutsTroopNameSerializer},
    )
    def create(self, request):
        input_serializer = ScoutsTroopNameSerializer(
            data=request.data, context={'request': request}
        )
        input_serializer.is_valid(raise_exception=True)

        name = ScoutsTroopNameService().name_create(
            **input_serializer.validated_data
        )

        output_serializer = ScoutsTroopNameSerializer(
            name, context={'request': request}
        )

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: ScoutsTroopNameSerializer}
    )
    def retrieve(self, request, pk=None):
        name = self.get_object()
        serializer = ScoutsTroopNameSerializer(
            name, context={'request': request}
        )

        return Response(serializer.data)
    
    @swagger_auto_schema(
        request_body=ScoutsTroopNameDeserializer,
        responses={status.HTTP_200_OK: ScoutsTroopNameSerializer},
    )
    def partial_update(self, request, pk=None):
        name = self.get_object()

        serializer = ScoutsTroopNameDeserializer(
            data=request.data,
            instance=name,
            context={'request': request},
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        updated_name = ScoutsTroopNameService().name_update(
            name=name, **serializer.validated_data
        )

        output_serializer = ScoutsTroopNameSerializer(
            updated_name, context={'request': request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: Schema(type=TYPE_STRING)}
    )
    def delete(self, request, pk):
        name = get_object_or_404(ScoutsTroopName.objects, pk=pk)
        name.delete()
        
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: ScoutsTroopNameSerializer}
    )
    def list(self, request):
        names = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(names)

        if page is not None:
            serializer = ScoutsTroopNameSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = ScoutsTroopNameSerializer(names, many=True)
            return Response(serializer.data)

