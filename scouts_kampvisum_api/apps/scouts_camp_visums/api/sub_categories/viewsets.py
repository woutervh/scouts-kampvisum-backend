from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.openapi import Schema, TYPE_STRING

from .models import ScoutsCampVisumSubCategory
from .services import ScoutsCampVisumSubCategoryService
from .serializers import ScoutsCampVisumSubCategorySerializer


class ScoutsCampVisumSubCategoryViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing and editing ScoutsCampVisumSubCategory instances.
    """
    
    serializer_class = ScoutsCampVisumSubCategorySerializer
    queryset = ScoutsCampVisumSubCategory.objects.all()
    
    @swagger_auto_schema(
        request_body=ScoutsCampVisumSubCategorySerializer,
        responses={
            status.HTTP_201_CREATED: ScoutsCampVisumSubCategorySerializer
        },
    )
    def create(self, request):
        """
        Creates a new ScoutsCampVisumSubCategory instance.
        """
        
        input_serializer = ScoutsCampVisumSubCategorySerializer(
            data=request.data, context={'request': request}
        )
        input_serializer.is_valid(raise_exception=True)

        instance = ScoutsCampVisumSubCategoryService().camp_create(
            **input_serializer.validated_data
        )

        output_serializer = ScoutsCampVisumSubCategorySerializer(
            instance, context={'request': request}
        )

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: ScoutsCampVisumSubCategorySerializer}
    )
    def retrieve(self, request, pk=None):
        """
        Gets and returns a ScoutsCampVisumSubCategory instance from the db.
        """
        
        instance = self.get_object()
        serializer = ScoutsCampVisumSubCategorySerializer(
            instance, context={'request': request}
        )

        return Response(serializer.data)
    
    @swagger_auto_schema(
        request_body=ScoutsCampVisumSubCategorySerializer,
        responses={status.HTTP_200_OK: ScoutsCampVisumSubCategorySerializer},
    )
    def partial_update(self, request, pk=None):
        """
        Updates a ScoutsCampVisumSubCategory instance.
        """
        
        instance = self.get_object()

        serializer = ScoutsCampVisumSubCategorySerializer(
            data=request.data,
            instance=instance,
            context={'request': request},
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        updated_instance = ScoutsCampVisumSubCategoryService().update(
            instance=instance, **serializer.validated_data
        )

        output_serializer = ScoutsCampVisumSubCategorySerializer(
            updated_instance, context={'request': request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: Schema(type=TYPE_STRING)}
    )
    def delete(self, request, pk):
        """
        Deletes a ScoutsCampVisumSubCategory instance.
        """
        
        instance = get_object_or_404(ScoutsCampVisumSubCategory.objects, pk=pk)
        instance.delete()
        
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: ScoutsCampVisumSubCategorySerializer}
    )
    def list(self, request):
        """
        Gets all ScoutsCampVisumSubCategory instances (filtered).
        """
        
        instances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = ScoutsCampVisumSubCategorySerializer(
                page, many=True
            )
            return self.get_paginated_response(serializer.data)
        else:
            serializer = ScoutsCampVisumSubCategorySerializer(
                instances, many=True
            )
            return Response(serializer.data)

