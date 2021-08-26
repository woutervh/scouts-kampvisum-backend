from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.openapi import Schema, TYPE_STRING

from ..models import CampVisumSubCategory
from ..services import CampVisumSubCategoryService
from ..serializers import CampVisumSubCategorySerializer


class CampVisumSubCategoryViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing and editing CampVisumSubCategory instances.
    """
    
    serializer_class = CampVisumSubCategorySerializer
    queryset = CampVisumSubCategory.objects.all()
    
    @swagger_auto_schema(
        request_body=CampVisumSubCategorySerializer,
        responses={
            status.HTTP_201_CREATED: CampVisumSubCategorySerializer
        },
    )
    def create(self, request):
        """
        Creates a new CampVisumSubCategory instance.
        """
        
        input_serializer = CampVisumSubCategorySerializer(
            data=request.data, context={'request': request}
        )
        input_serializer.is_valid(raise_exception=True)

        instance = CampVisumSubCategoryService().camp_create(
            **input_serializer.validated_data
        )

        output_serializer = CampVisumSubCategorySerializer(
            instance, context={'request': request}
        )

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: CampVisumSubCategorySerializer}
    )
    def retrieve(self, request, pk=None):
        """
        Gets and returns a CampVisumSubCategory instance from the db.
        """
        
        instance = self.get_object()
        serializer = CampVisumSubCategorySerializer(
            instance, context={'request': request}
        )

        return Response(serializer.data)
    
    @swagger_auto_schema(
        request_body=CampVisumSubCategorySerializer,
        responses={status.HTTP_200_OK: CampVisumSubCategorySerializer},
    )
    def partial_update(self, request, pk=None):
        """
        Updates a CampVisumSubCategory instance.
        """
        
        instance = self.get_object()

        serializer = CampVisumSubCategorySerializer(
            data=request.data,
            instance=instance,
            context={'request': request},
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        updated_instance = CampVisumSubCategoryService().update(
            instance=instance, **serializer.validated_data
        )

        output_serializer = CampVisumSubCategorySerializer(
            updated_instance, context={'request': request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: Schema(type=TYPE_STRING)}
    )
    def delete(self, request, pk):
        """
        Deletes a CampVisumSubCategory instance.
        """
        
        instance = get_object_or_404(CampVisumSubCategory.objects, pk=pk)
        instance.delete()
        
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: CampVisumSubCategorySerializer}
    )
    def list(self, request):
        """
        Gets all CampVisumSubCategory instances (filtered).
        """
        
        instances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = CampVisumSubCategorySerializer(
                page, many=True
            )
            return self.get_paginated_response(serializer.data)
        else:
            serializer = CampVisumSubCategorySerializer(
                instances, many=True
            )
            return Response(serializer.data)

