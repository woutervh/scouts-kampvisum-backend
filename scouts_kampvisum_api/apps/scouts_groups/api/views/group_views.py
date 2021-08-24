import logging
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg2.utils import swagger_auto_schema

from ..models import ScoutsGroup
from ..services import ScoutsGroupService
from ..serializers import (
    ScoutsGroupSerializer,
    ScoutsSectionSerializer,
    ScoutsSectionCreationAPISerializer,
    ScoutsSectionAPISerializer,
)


logger = logging.getLogger(__name__)


class ScoutsGroupViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing scout groups for the current user.
    """
    
    service = ScoutsGroupService()
    lookup_field = 'uuid'
    serializer_class = ScoutsGroupSerializer
    queryset = ScoutsGroup.objects.all()
    
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: ScoutsGroupSerializer}
    )
    def retrieve(self, request, pk=None):
        """
        Retrieves an existing ScoutGroup object.
        """
        
        instance = self.get_object()
        serializer = ScoutsGroupSerializer(
            instance, context={'request': request}
        )

        return Response(serializer.data)
    
    @action(
        detail=False, methods=['get'], permission_classes=[IsAuthenticated],
        url_path='import')
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: ScoutsGroupSerializer}
    )
    def import_groups(self, request, pk=None):
        """
        Retrieves authorized groups from GroupAdmin and stores them.
        """
        user = request.user
        groups = self.service.import_groupadmin_groups(user)
        page = self.paginate_queryset(groups)
        
        if page is not None:
            serializer = ScoutsGroupSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = ScoutsGroupSerializer(groups, many=True)
            return Response(serializer.data)
    
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: ScoutsGroupSerializer}
    )
    def list(self, request):
        """
        Retrieves a list of all existing ScoutsGroup instances.
        """
        
        user = request.user
        groups = [group.id for group in user.partial_scouts_groups]
        
        instances = ScoutsGroup.objects.filter(group_admin_id__in=groups)
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = ScoutsGroupSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = ScoutsGroupSerializer(instances, many=True)
            return Response(serializer.data)
    
    def _get_group(self, key, value):
        filters = {key : value}
        qs = ScoutsGroup.objects.filter(**filters)

        if qs.count() == 1:
            return qs[0]
        
        return None

    @action(
        detail=True, methods=['get', 'post'], permission_classes=[IsAuthenticated],
        url_path='sections')
    @swagger_auto_schema(
        request_body=ScoutsSectionCreationAPISerializer,
        responses={status.HTTP_200_OK: ScoutsSectionSerializer},
    )
    def sections(self, request, uuid=None):
        """
        Retrieves a list of sections for this ScoutsGroup.
        """
        if request.method == 'POST':
            return self._add_sections(request, uuid)
        else:
            return self._get_sections(request, uuid)
    
    def _add_sections(self, request, uuid=None):
        """
        Creates and add ScoutsSections to the given ScoutsGroup.
        """
        input_serializer = ScoutsSectionCreationAPISerializer(
            data=request.data, context={'request': request}
        )
        input_serializer.is_valid(raise_exception=True)

        logger.debug('REQUEST DATA: %s', request.data)

        instance = self.get_object()
        instance = ScoutsGroupService().add_section(
            instance,
            **input_serializer.validated_data
        )

        output_serializer = ScoutsGroupSerializer(
            instance, context={'request': request}
        )

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    
    def _get_sections(self, request, uuid=None):
        """
        Returns ScoutsSection instances associated with the given ScoutsGroup.
        """
        logger.debug('Searching for sections for group with uuid %s', uuid)
        
        instance = get_object_or_404(ScoutsGroup, uuid=uuid)
        instances = instance.sections.filter(hidden=False).distinct()

        logger.debug(
            'Found %s instance(s) that are not hidden', len(instances))

        if len(instances) == 0:
            logger.warn('No sections defined for group with uuid %s\
                - Did you forget to call setup ?', instance.uuid)

        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = ScoutsSectionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = ScoutsSectionSerializer(instances, many=True)
            return Response(serializer.data)

        return Response(output_serializer.data)
    
    @action(
        detail=True, methods=['get'], permission_classes=[IsAuthenticated],
        url_path='camps')
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: ScoutsSectionSerializer},
    )
    def get_camps(self, request, uuid=None):
        """
        """

