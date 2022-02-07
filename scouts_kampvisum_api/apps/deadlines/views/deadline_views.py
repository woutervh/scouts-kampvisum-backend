import logging

from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.openapi import Schema, TYPE_STRING

from apps.deadlines.models import (Deadline, SubCategoryDeadline, CheckDeadline, DeadlineDependentDeadline)
from apps.deadlines.serializers import (DeadlineSerializer, SubCategoryDeadlineSerializer, CheckDeadlineSerializer, DeadlineDependentDeadlineSerializer)
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

        instance = self.deadline_service.create_deadline(request, **validated_data)

        output_serializer = DeadlineSerializer(instance, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: DeadlineSerializer})
    def retrieve(self, request, pk=None):
        instance: Deadline = get_object_or_404(Deadline.objects, pk=pk)
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

        output_serializer = DeadlineSerializer(
            instance, context={"request": request}
        )

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
        request_body=SubCategoryDeadlineSerializer,
        responses={status.HTTP_201_CREATED: SubCategoryDeadlineSerializer},
    )
    def create_sub_category_deadline(self, request):
        """
        Creates a new sub_category deadline instance.
        """
        logger.debug("SUB CATEGORY DEADLINE CREATE REQUEST DATA: %s", request.data)
        input_serializer = SubCategoryDeadlineSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("SUB CATEGORY DEADLINE CREATE VALIDATED DATA: %s", validated_data)

        instance = self.deadline_service.create_sub_category_deadline(request, **validated_data)

        output_serializer = SubCategoryDeadlineSerializer(instance, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: SubCategoryDeadlineSerializer})
    def retrieve_sub_category_deadline(self, request, deadline_id=None):
        instance: SubCategoryDeadline = self.deadline_service.get_sub_category_deadline(deadline_id)
        serializer = SubCategoryDeadlineSerializer(instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=SubCategoryDeadlineSerializer,
        responses={status.HTTP_200_OK: SubCategoryDeadlineSerializer},
    )
    def partial_update_sub_category_deadline(self, request, deadline_id):
        logger.debug("SUB CATEGORY DEADLINE UPDATE REQUEST DATA: %s", request.data)
        instance: SubCategoryDeadline = self.deadline_service.get_sub_category_deadline(
            deadline_id
        )

        serializer = SubCategoryDeadlineSerializer(
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

        output_serializer = SubCategoryDeadlineSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get"],
        url_path=r"sub_category"
    )
    @swagger_auto_schema(responses={status.HTTP_200_OK: SubCategoryDeadlineSerializer})
    def list_sub_category_deadlines(self, request):
        logger.debug("Listing SubCategoryDeadline instances")
        instances = self.filter_queryset(SubCategoryDeadline.objects.all())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = SubCategoryDeadlineSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)
        else:
            serializer = SubCategoryDeadlineSerializer(
                instances, many=True, context={"request": request}
            )
            return Response(serializer.data)
    
    @swagger_auto_schema(
        request_body=CheckDeadlineSerializer,
        responses={status.HTTP_201_CREATED: CheckDeadlineSerializer},
    )
    def create_check_deadline(self, request):
        """
        Creates a new check deadline instance.
        """
        logger.debug("CHECK DEADLINE CREATE REQUEST DATA: %s", request.data)
        input_serializer = CheckDeadlineSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("CHECK DEADLINE CREATE VALIDATED DATA: %s", validated_data)

        instance = self.deadline_service.create_check_deadline(request, **validated_data)

        output_serializer = CheckDeadlineSerializer(instance, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CheckDeadlineSerializer})
    def retrieve_check_deadline(self, request, deadline_id=None):
        instance: CheckDeadline = self.deadline_service.get_check_deadline(deadline_id)
        serializer = CheckDeadlineSerializer(instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CheckDeadlineSerializer,
        responses={status.HTTP_200_OK: CheckDeadlineSerializer},
    )
    def partial_update_check_deadline(self, request, deadline_id):
        logger.debug("CHECK DEADLINE UPDATE REQUEST DATA: %s", request.data)
        instance: CheckDeadline = self.deadline_service.get_check_deadline(
            deadline_id
        )

        serializer = CheckDeadlineSerializer(
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

        output_serializer = CheckDeadlineSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CheckDeadlineSerializer})
    def list_check_deadlines(self, request):
        instances = self.filter_queryset(CheckDeadline.objects.all())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = CheckDeadlineSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)
        else:
            serializer = CheckDeadlineSerializer(
                instances, many=True, context={"request": request}
            )
            return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: DeadlineDependentDeadlineSerializer})
    def retrieve_deadline_dependent_deadline(self, request, deadline_id=None):
        instance: DeadlineDependentDeadline = self.deadline_service.get_deadline_dependent_deadline(deadline_id)
        serializer = DeadlineDependentDeadlineSerializer(instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=DeadlineDependentDeadlineSerializer,
        responses={status.HTTP_200_OK: DeadlineDependentDeadlineSerializer},
    )
    def partial_update_deadline_dependent_deadline(self, request, deadline_id):
        logger.debug("DEADLINE DEPENDENT DEADLINE UPDATE REQUEST DATA: %s", request.data)
        instance: DeadlineDependentDeadline = self.deadline_service.get_deadline_dependent_deadline(
            deadline_id
        )

        serializer = DeadlineDependentDeadlineSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("DEADLINE DEPENDENT DEADLINE UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.deadline_service.update_deadline_dependent_deadline(
            instance, **validated_data
        )

        output_serializer = DeadlineDependentDeadlineSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get"],
        url_path="deadline_dependent",
    )
    @swagger_auto_schema(responses={status.HTTP_200_OK: DeadlineDependentDeadlineSerializer})
    def list_sub_category_deadlines(self, request):
        instances = self.filter_queryset(DeadlineDependentDeadline.objects.all())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = DeadlineDependentDeadlineSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)
        else:
            serializer = DeadlineDependentDeadlineSerializer(
                instances, many=True, context={"request": request}
            )
            return Response(serializer.data)