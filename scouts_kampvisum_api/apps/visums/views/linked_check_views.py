import logging

from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from apps.visums.models import (
    LinkedCheck,
    LinkedSimpleCheck,
    LinkedDateCheck,
    LinkedDurationCheck,
    LinkedLocationCheck,
    LinkedMemberCheck,
    LinkedFileUploadCheck,
    LinkedCommentCheck,
)
from apps.visums.serializers import (
    LinkedCheckSerializer,
    LinkedSimpleCheckSerializer,
    LinkedDateCheckSerializer,
    LinkedDurationCheckSerializer,
    LinkedLocationCheckSerializer,
    LinkedCampLocationCheckSerializer,
    LinkedMemberCheckSerializer,
    LinkedFileUploadCheckSerializer,
    LinkedCommentCheckSerializer,
)
from apps.visums.services import LinkedCheckService


logger = logging.getLogger(__name__)


class LinkedCheckViewSet(viewsets.GenericViewSet):
    """
    A viewset for LinkedCheck instances.
    """

    serializer_class = LinkedCheckSerializer
    queryset = LinkedCheck.objects.all()
    filter_backends = [filters.DjangoFilterBackend]

    linked_check_service = LinkedCheckService()

    def get_simple_check(self, check: LinkedCheck):
        return LinkedSimpleCheck()

    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedCheckSerializer})
    def retrieve(self, request, pk=None):
        instance: LinkedCheck = get_object_or_404(LinkedCheck.objects, pk=pk)
        serializer = LinkedCheckSerializer(instance, context={"request": request})

        return Response(serializer.data)

    # @swagger_auto_schema(
    #     request_body=LinkedCheckSerializer,
    #     responses={status.HTTP_200_OK: LinkedCheckSerializer},
    # )
    # def partial_update(self, request, pk):
    #     instance = self.get_object()

    #     logger.debug("LINKED CHECK UPDATE REQUEST DATA: %s", request.data)

    #     serializer = LinkedCheckSerializer(
    #         data=request.data,
    #         instance=instance,
    #         context={"request": request},
    #         partial=True,
    #     )
    #     serializer.is_valid(raise_exception=True)

    #     validated_data = serializer.validated_data
    #     logger.debug("LINKED CHECK UPDATE VALIDATED DATA: %s", validated_data)

    #     logger.debug("Updating LinkedCheck with id %s", pk)

    #     updated_instance = self.camp_visum_service.visum_update(
    #         request, instance=instance, **validated_data
    #     )

    #     output_serializer = LinkedCheckSerializer(
    #         updated_instance, context={"request": request}
    #     )

    #     return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=LinkedSimpleCheckSerializer,
        responses={status.HTTP_200_OK: LinkedSimpleCheckSerializer},
    )
    def partial_update_simple_check(self, request, check_id):
        instance = self.linked_check_service.get_simple_check(check_id)

        logger.debug("SIMPLE CHECK UPDATE REQUEST DATA: %s", request.data)
        serializer = LinkedSimpleCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("SIMPLE CHECK UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.update_simple_check(
            instance, **validated_data
        )

        output_serializer = LinkedSimpleCheckSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=LinkedDurationCheckSerializer,
        responses={status.HTTP_200_OK: LinkedDurationCheckSerializer},
    )
    def partial_update_duration_check(self, request, check_id):
        instance = self.linked_check_service.get_duration_check(check_id)

        logger.debug("DURATION CHECK UPDATE REQUEST DATA: %s", request.data)
        serializer = LinkedDurationCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("DURATION CHECK UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.update_duration_check(
            instance, **validated_data
        )

        output_serializer = LinkedDurationCheckSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=LinkedLocationCheckSerializer,
        responses={status.HTTP_200_OK: LinkedLocationCheckSerializer},
    )
    def partial_update_location_check(self, request, check_id):
        instance = self.linked_check_service.get_location_check(check_id)

        logger.debug("LOCATION CHECK UPDATE REQUEST DATA: %s", request.data)
        serializer = LinkedLocationCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("LOCATION CHECK UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.update_location_check(
            instance, **validated_data
        )

        output_serializer = LinkedLocationCheckSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=LinkedCampLocationCheckSerializer,
        responses={status.HTTP_200_OK: LinkedCampLocationCheckSerializer},
    )
    def partial_update_camp_location_check(self, request, check_id):
        instance = self.linked_check_service.get_camp_location_check(check_id)

        logger.debug("CAMP LOCATION CHECK UPDATE REQUEST DATA: %s", request.data)
        serializer = LinkedCampLocationCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("CAMP LOCATION CHECK UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.update_camp_location_check(
            instance, **validated_data
        )

        output_serializer = LinkedCampLocationCheckSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=LinkedFileUploadCheckSerializer,
        responses={status.HTTP_200_OK: LinkedFileUploadCheckSerializer},
    )
    def partial_update_file_upload_check(self, request, check_id):
        instance = self.linked_check_service.get_file_upload_check(check_id)

        logger.debug("FILE UPLOAD CHECK UPDATE REQUEST DATA: %s", request.data)
        serializer = LinkedFileUploadCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("FILE UPLOAD CHECK UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.update_file_upload_check(
            instance=instance, uploaded_file=validated_data.get("value")
        )

        output_serializer = LinkedFileUploadCheckSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=LinkedCommentCheckSerializer,
        responses={status.HTTP_200_OK: LinkedCommentCheckSerializer},
    )
    def partial_update_comment_check(self, request, check_id):
        instance = self.linked_check_service.get_comment_check(check_id)

        logger.debug("COMMENT CHECK UPDATE REQUEST DATA: %s", request.data)
        serializer = LinkedCommentCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("COMMENT CHECK UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.update_comment_check(
            instance, **validated_data
        )

        output_serializer = LinkedCommentCheckSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedCheckSerializer})
    def list(self, request):
        """
        Gets all Check instances (filtered).
        """

        instances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = LinkedCheckSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = LinkedCheckSerializer(instances, many=True)
            return Response(serializer.data)
