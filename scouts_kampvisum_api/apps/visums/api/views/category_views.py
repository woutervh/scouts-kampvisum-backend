from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.openapi import Schema, TYPE_STRING

from ..models import CampVisumCategory
from ..services import CampVisumCategoryService
from ..serializers import (
    CampVisumCategorySerializer,
    CampVisumSubCategorySerializer
)


class CampVisumCategoryViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing and editing CampVisumCategory instances.
    """

    serializer_class = CampVisumCategorySerializer
    queryset = CampVisumCategory.objects.all()

    @swagger_auto_schema(
        request_body=CampVisumCategorySerializer,
        responses={status.HTTP_201_CREATED: CampVisumCategorySerializer},
    )
    def create(self, request):
        """
        Creates a new CampVisumCategory instance.
        """

        input_serializer = CampVisumCategorySerializer(
            data=request.data, context={'request': request}
        )
        input_serializer.is_valid(raise_exception=True)

        instance = CampVisumCategoryService().camp_create(
            **input_serializer.validated_data
        )

        output_serializer = CampVisumCategorySerializer(
            instance, context={'request': request}
        )

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: CampVisumCategorySerializer}
    )
    def retrieve(self, request, pk=None):
        """
        Gets and returns a CampVisumCategory instance from the db.
        """

        instance = self.get_object()
        serializer = CampVisumCategorySerializer(
            instance, context={'request': request}
        )

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CampVisumCategorySerializer,
        responses={status.HTTP_200_OK: CampVisumCategorySerializer},
    )
    def partial_update(self, request, pk=None):
        """
        Updates a CampVisumCategory instance.
        """

        instance = self.get_object()

        serializer = CampVisumCategorySerializer(
            data=request.data,
            instance=instance,
            context={'request': request},
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        updated_instance = CampVisumCategoryService().update(
            instance=instance, **serializer.validated_data
        )

        output_serializer = CampVisumCategorySerializer(
            updated_instance, context={'request': request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: Schema(type=TYPE_STRING)}
    )
    def delete(self, request, pk):
        """
        Deletes a CampVisumCategory instance.
        """

        instance = get_object_or_404(CampVisumCategory.objects, pk=pk)
        instance.delete()

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: CampVisumCategorySerializer}
    )
    def list(self, request):
        """
        Gets all CampVisumCategory instances (filtered).
        """

        instances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = CampVisumCategorySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = CampVisumCategorySerializer(
                instances, many=True)
            return Response(serializer.data)

    @action(
        detail=True, methods=['get'], permission_classes=[IsAuthenticated],
        url_path='sub-categories')
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: CampVisumSubCategorySerializer},
    )
    def sub_categories(self, request, pk=None):
        """
        Retrieves a list of sub-categories for this ScoutsKampVisumCategory.
        """

        instance = self.get_object()
        instances = instance.sub_categories.all().order_by('name')

        output_serializer = CampVisumSubCategorySerializer(
            instances, many=True)

        return Response(output_serializer.data)
