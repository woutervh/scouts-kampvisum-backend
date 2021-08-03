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
from .models import Camp
from .services import CampService
from .serializers import CampOutputSerializer, CampInputSerializer


class CampViewSet(viewsets.GenericViewSet):
    '''A viewset for viewing and editing camp instances.'''
    
    serializer_class = CampOutputSerializer
    queryset = Camp.objects.all()
    
    @swagger_auto_schema(
        request_body=CampInputSerializer,
        responses={status.HTTP_201_CREATED: CampOutputSerializer},
    )
    def create(self, request):
        input_serializer = CampInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        camp = CampService.camp_create(
            **input_serializer.validated_data
        )

        output_serializer = CampOutputSerializer(camp, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: CampOutputSerializer})
    def retrieve(self, request, pk=None):
        camp = self.get_object()
        serializer = CampOutputSerializer(camp, context={"request": request})

        return Response(serializer.data)
    
    @swagger_auto_schema(
        request_body=CampInputSerializer,
        responses={status.HTTP_200_OK: CampOutputSerializer},
    )
    def partial_update(self, request, pk=None):
        camp = self.get_object()

        serializer = CampInputSerializer(
            data=request.data, instance=camp, context={"request": request}, partial=True
        )
        serializer.is_valid(raise_exception=True)

        updated_camp = CampService.camp_update(camp=camp, **serializer.validated_data)

        output_serializer = CampOutputSerializer(updated_camp, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: Schema(type=TYPE_STRING)}
    )
    def delete(self, request, pk):
        camp = get_object_or_404(Camp.objects, pk=pk)
        camp.delete()
        
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: CampOutputSerializer})
    def list(self, request):
        equipment = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(equipment)

        if page is not None:
            serializer = CampOutputSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = CampOutputSerializer(equipment, many=True)
            return Response(serializer.data)

