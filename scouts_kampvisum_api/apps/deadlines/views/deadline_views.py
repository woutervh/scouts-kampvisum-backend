import logging
from typing import List

from django.core.exceptions import ValidationError
from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema

from apps.deadlines.models import (
    Deadline,
    LinkedSubCategoryDeadline,
    LinkedCheckDeadline,
    MixedDeadline,
    DeadlineFlag,
)
from apps.deadlines.serializers import (
    DeadlineSerializer,
    LinkedSubCategoryDeadlineSerializer,
    LinkedCheckDeadlineSerializer,
    MixedDeadlineSerializer,
    VisumDeadlineSerializer,
    DeadlineFlagSerializer,
)
from apps.deadlines.services import DeadlineService


logger = logging.getLogger(__name__)


class DeadlineViewSet(viewsets.GenericViewSet):
    """
    A viewset for Deadline instances.
    """

    serializer_class = DeadlineSerializer
    queryset = Deadline.objects.all()
    filter_backends = [filters.DjangoFilterBackend]

    deadline_service = DeadlineService()

    @swagger_auto_schema(
        request_body=DeadlineSerializer,
        responses={status.HTTP_201_CREATED: DeadlineSerializer},
    )
    def create(self, request):
        """
        Creates a new deadline instance.
        """
        logger.debug("DEADLINE CREATE REQUEST DATA: %s", request.data)
        input_serializer = DeadlineSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("DEADLINE CREATE VALIDATED DATA: %s", validated_data)

        instance = self.deadline_service.get_or_create_deadline(
            request, **validated_data
        )

        output_serializer = DeadlineSerializer(instance, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: DeadlineSerializer})
    def retrieve(self, request, pk=None):
        instance: Deadline = Deadline.objects.safe_get(pk=pk, raise_error=True)
        serializer = DeadlineSerializer(instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=DeadlineSerializer,
        responses={status.HTTP_200_OK: DeadlineSerializer},
    )
    def partial_update(self, request, pk):
        logger.debug("DEADLINE UPDATE REQUEST DATA: %s", request.data)
        instance: Deadline = self.deadline_service.get_deadline(deadline_id=pk)

        serializer = DeadlineSerializer(
            instance=instance,
            data=request.data,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("DEADLINE UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.deadline_service.update_deadline(
            request, instance, **validated_data
        )

        output_serializer = DeadlineSerializer(instance, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={status.HTTP_200_OK: DeadlineSerializer})
    def list(self, request):
        """
        Gets all Deadline instances (filtered).
        """

        instances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = DeadlineSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)
        else:
            serializer = DeadlineSerializer(
                instances, many=True, context={"request": request}
            )
            return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedSubCategoryDeadlineSerializer,
        responses={status.HTTP_201_CREATED: LinkedSubCategoryDeadlineSerializer},
    )
    def create_linked_sub_category_deadline(self, request):
        """
        Creates a new sub_category deadline instance.
        """
        logger.debug("SUB CATEGORY DEADLINE CREATE REQUEST DATA: %s", request.data)
        input_serializer = LinkedSubCategoryDeadlineSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("SUB CATEGORY DEADLINE CREATE VALIDATED DATA: %s", validated_data)

        instance = self.deadline_service.get_or_create_linked_sub_category_deadline(
            request, **validated_data
        )

        output_serializer = LinkedSubCategoryDeadlineSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: LinkedSubCategoryDeadlineSerializer}
    )
    def retrieve_linked_sub_category_deadline(self, request, deadline_id=None):
        instance: LinkedSubCategoryDeadline = (
            LinkedSubCategoryDeadline.objects.safe_get(id=deadline_id, raise_error=True)
        )
        serializer = LinkedSubCategoryDeadlineSerializer(
            instance, context={"request": request}
        )

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedSubCategoryDeadlineSerializer,
        responses={status.HTTP_200_OK: LinkedSubCategoryDeadlineSerializer},
    )
    def partial_update_sub_category_deadline(self, request, deadline_id):
        logger.debug("SUB CATEGORY DEADLINE UPDATE REQUEST DATA: %s", request.data)
        instance: LinkedSubCategoryDeadline = (
            LinkedSubCategoryDeadline.objects.safe_get(id=deadline_id, raise_error=True)
        )

        serializer = LinkedSubCategoryDeadlineSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("SUB CATEGORY DEADLINE UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.deadline_service.update_deadline(
            request, instance, **validated_data
        )

        output_serializer = LinkedSubCategoryDeadlineSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path=r"sub_category")
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: LinkedSubCategoryDeadlineSerializer}
    )
    def list_linked_sub_category_deadlines(self, request):
        logger.debug("Listing SubCategoryDeadline instances")
        instances = self.filter_queryset(LinkedSubCategoryDeadline.objects.all())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = LinkedSubCategoryDeadlineSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)
        else:
            serializer = LinkedSubCategoryDeadlineSerializer(
                instances, many=True, context={"request": request}
            )
            return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedCheckDeadlineSerializer,
        responses={status.HTTP_201_CREATED: LinkedCheckDeadlineSerializer},
    )
    def create_linked_check_deadline(self, request):
        """
        Creates a new check deadline instance.
        """
        logger.debug("CHECK DEADLINE CREATE REQUEST DATA: %s", request.data)
        input_serializer = LinkedCheckDeadlineSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("CHECK DEADLINE CREATE VALIDATED DATA: %s", validated_data)

        instance = self.deadline_service.get_or_create_linked_check_deadline(
            request, **validated_data
        )

        output_serializer = LinkedCheckDeadlineSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedCheckDeadlineSerializer})
    def retrieve_linked_check_deadline(self, request, deadline_id=None):
        instance: LinkedCheckDeadline = LinkedCheckDeadline.objects.safe_get(
            id=deadline_id, raise_error=True
        )
        serializer = LinkedCheckDeadlineSerializer(
            instance, context={"request": request}
        )

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedCheckDeadlineSerializer,
        responses={status.HTTP_200_OK: LinkedCheckDeadlineSerializer},
    )
    def partial_update_linked_check_deadline(self, request, deadline_id):
        logger.debug("CHECK DEADLINE UPDATE REQUEST DATA: %s", request.data)
        instance: LinkedCheckDeadline = LinkedCheckDeadline.objects.safe_get(
            id=deadline_id, raise_error=True
        )

        serializer = LinkedCheckDeadlineSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("CHECK DEADLINE UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.deadline_service.update_deadline(
            request, instance, **validated_data
        )

        output_serializer = LinkedCheckDeadlineSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedCheckDeadlineSerializer})
    def list_linked_check_deadlines(self, request):
        instances = self.filter_queryset(LinkedCheckDeadline.objects.all())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = LinkedCheckDeadlineSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)
        else:
            serializer = LinkedCheckDeadlineSerializer(
                instances, many=True, context={"request": request}
            )
            return Response(serializer.data)

    @swagger_auto_schema(
        request_body=MixedDeadlineSerializer,
        responses={status.HTTP_201_CREATED: MixedDeadlineSerializer},
    )
    def create_mixed_deadline(self, request):
        """
        Creates a new mixed deadline instance.
        """
        logger.debug("MIXED DEADLINE CREATE REQUEST DATA: %s", request.data)
        input_serializer = MixedDeadlineSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("MIXED DEADLINE CREATE VALIDATED DATA: %s", validated_data)

        instance = self.deadline_service.get_or_create_mixed_deadline(
            request, **validated_data
        )

        output_serializer = MixedDeadlineSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: MixedDeadlineSerializer})
    def retrieve_mixed_deadline(self, request, deadline_id=None):
        instance: MixedDeadline = MixedDeadline.objects.safe_get(
            id=deadline_id, raise_error=True
        )
        serializer = MixedDeadlineSerializer(instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=MixedDeadlineSerializer,
        responses={status.HTTP_200_OK: MixedDeadlineSerializer},
    )
    def partial_update_mixed_deadline(self, request, deadline_id):
        logger.debug("MIXED DEADLINE UPDATE REQUEST DATA: %s", request.data)
        instance: MixedDeadline = MixedDeadline.objects.safe_get(
            id=deadline_id, raise_error=True
        )

        serializer = MixedDeadlineSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("MIXED DEADLINE UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.deadline_service.update_deadline(
            request, instance, **validated_data
        )

        output_serializer = MixedDeadlineSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={status.HTTP_200_OK: MixedDeadlineSerializer})
    def list_mixed_deadlines(self, request):
        instances = self.filter_queryset(MixedDeadline.objects.all())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = MixedDeadlineSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)
        else:
            serializer = MixedDeadlineSerializer(
                instances, many=True, context={"request": request}
            )
            return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: VisumDeadlineSerializer})
    def list_for_visum(self, request, visum_id):
        logger.debug("Loading deadlines for visum %s", visum_id)

        instances = self.filter_queryset(
            self.deadline_service.list_for_visum(visum=visum_id)
        )
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = VisumDeadlineSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)
        else:
            serializer = VisumDeadlineSerializer(
                instances, many=True, context={"request": request}
            )
            return Response(serializer.data)

    @swagger_auto_schema(
        request_body=DeadlineFlagSerializer,
        responses={status.HTTP_200_OK: VisumDeadlineSerializer},
    )
    def partial_update_deadline_flag(self, request, deadline_flag_id):
        logger.debug("DEADLINE FLAG UPDATE REQUEST DATA: %s", request.data)
        instance: DeadlineFlag = DeadlineFlag.objects.safe_get(
            id=deadline_flag_id, raise_error=True
        )

        serializer = DeadlineFlagSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("DEADLINE FLAG UPDATE VALIDATED DATA: %s", validated_data)

        instance: DeadlineFlag = self.deadline_service.update_deadline_flag(
            request, instance, **validated_data
        )

        instance: Deadline = self.deadline_service.get_visum_deadline(
            deadline=instance.deadline
        )
        serializer = VisumDeadlineSerializer(instance, context={"request": request})

        return Response(serializer.data)
