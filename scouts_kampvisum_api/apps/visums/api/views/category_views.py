from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.openapi import Schema, TYPE_STRING

from ..models import Category
from ..services import CategoryService
from ..serializers import CategorySerializer, SubCategorySerializer


class CategoryViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing and editing Category instances.
    """

    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    @swagger_auto_schema(
        request_body=CategorySerializer,
        responses={status.HTTP_201_CREATED: CategorySerializer},
    )
    def create(self, request):
        """
        Creates a new Category instance.
        """

        input_serializer = CategorySerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        instance = CategoryService().camp_create(**input_serializer.validated_data)

        output_serializer = CategorySerializer(instance, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CategorySerializer})
    def retrieve(self, request, pk=None):
        """
        Gets and returns a Category instance from the db.
        """

        instance = self.get_object()
        serializer = CategorySerializer(instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CategorySerializer,
        responses={status.HTTP_200_OK: CategorySerializer},
    )
    def partial_update(self, request, pk=None):
        """
        Updates a Category instance.
        """

        instance = self.get_object()

        serializer = CategorySerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        updated_instance = CategoryService().update(
            instance=instance, **serializer.validated_data
        )

        output_serializer = CategorySerializer(
            updated_instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: Schema(type=TYPE_STRING)}
    )
    def delete(self, request, pk):
        """
        Deletes a Category instance.
        """

        instance = get_object_or_404(Category.objects, pk=pk)
        instance.delete()

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CategorySerializer})
    def list(self, request):
        """
        Gets all Category instances (filtered).
        """

        instances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = CategorySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = CategorySerializer(instances, many=True)
            return Response(serializer.data)

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="sub-categories",
    )
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: SubCategorySerializer},
    )
    def sub_categories(self, request, pk=None):
        """
        Retrieves a list of sub-categories for this ScoutsKampVisumCategory.
        """

        instance = self.get_object()
        instances = instance.sub_categories.all().order_by("name")

        output_serializer = SubCategorySerializer(instances, many=True)

        return Response(output_serializer.data)
