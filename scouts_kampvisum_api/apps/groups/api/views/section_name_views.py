import logging
from django.http.response import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.openapi import Schema, TYPE_STRING

from ..models import SectionName
from ..services import SectionNameService
from ..serializers import SectionNameSerializer


logger = logging.getLogger(__name__)


class SectionNameViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing and editing scout section names.
    """

    lookup_field = 'uuid'
    serializer_class = SectionNameSerializer
    queryset = SectionName.objects.all()

    @swagger_auto_schema(
        request_body=SectionNameSerializer,
        responses={status.HTTP_201_CREATED: SectionNameSerializer},
    )
    def create(self, request):
        """
        Creates a new ScoutSectionName.
        """
        input_serializer = SectionNameSerializer(
            data=request.data, context={'request': request}
        )
        input_serializer.is_valid(raise_exception=True)

        instance = SectionNameService().name_create(
            **input_serializer.validated_data
        )

        output_serializer = SectionNameSerializer(
            instance, context={'request': request}
        )

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: SectionNameSerializer}
    )
    def retrieve(self, request, uuid=None):
        """
        Retrieves an existing ScoutSectionName object.
        """
        instance = self.get_object()
        serializer = SectionNameSerializer(
            instance, context={'request': request}
        )

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=SectionNameSerializer,
        responses={status.HTTP_200_OK: SectionNameSerializer},
    )
    def partial_update(self, request, uuid=None):
        """
        Updates an existing SectionName object.
        """
        instance = self.get_object()

        serializer = SectionNameSerializer(
            data=request.data,
            instance=instance,
            context={'request': request},
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        updated_instance = SectionNameService().name_update(
            instance=instance, **serializer.validated_data
        )

        output_serializer = SectionNameSerializer(
            updated_instance, context={'request': request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: SectionNameSerializer}
    )
    def list(self, request):
        """
        Retrieves a list of all existing SectionName instances.
        """

        instances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = SectionNameSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = SectionNameSerializer(instances, many=True)
            return Response(serializer.data)

    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: Schema(type=TYPE_STRING)}
    )
    def delete(self, request, uuid):
        """
        Deletes a SectionName instance by uuid
        """
        instance = SectionName.objects.get(uuid=uuid)

        if not instance:
            logger.error(
                "No SectionName found with uuid '%s'", uuid)
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        instance.delete()

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
