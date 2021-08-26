import logging
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg2.utils import swagger_auto_schema

from ..models import Group
from ..services import GroupService
from ..serializers import (
    GroupSerializer,
    SectionSerializer,
    SectionCreationAPISerializer,
    SectionAPISerializer,
)


logger = logging.getLogger(__name__)


class GroupViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing scout groups for the current user.
    """

    service = GroupService()
    lookup_field = 'uuid'
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: GroupSerializer}
    )
    def retrieve(self, request, pk=None):
        """
        Retrieves an existing ScoutGroup object.
        """

        instance = self.get_object()
        serializer = GroupSerializer(
            instance, context={'request': request}
        )

        return Response(serializer.data)

    @action(
        detail=False, methods=['get'], permission_classes=[IsAuthenticated],
        url_path='import')
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: GroupSerializer}
    )
    def import_groups(self, request, pk=None):
        """
        Retrieves authorized groups from GroupAdmin and stores them.
        """
        user = request.user
        groups = self.service.import_groupadmin_groups(user)
        page = self.paginate_queryset(groups)

        if page is not None:
            serializer = GroupSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = GroupSerializer(groups, many=True)
            return Response(serializer.data)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: GroupSerializer}
    )
    def list(self, request):
        """
        Retrieves a list of all existing Group instances.
        """

        user = request.user
        groups = [group.id for group in user.partial_scouts_groups]

        instances = Group.objects.filter(group_admin_id__in=groups)
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = GroupSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = GroupSerializer(instances, many=True)
            return Response(serializer.data)

    def _get_group(self, key, value):
        filters = {key: value}
        qs = Group.objects.filter(**filters)

        if qs.count() == 1:
            return qs[0]

        return None

    @action(
        detail=True, methods=['get', 'post'], permission_classes=[IsAuthenticated],
        url_path='sections')
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: SectionSerializer},
    )
    def sections(self, request, uuid=None):
        """
        Retrieves a list of sections for this Group.
        """
        if request.method == 'POST':
            return self._add_sections(request, uuid)
        else:
            return self._get_sections(request, uuid)

    def _add_sections(self, request, uuid=None):
        """
        Creates and add Sections to the given Group.
        """
        input_serializer = SectionCreationAPISerializer(
            data=request.data, context={'request': request}
        )
        input_serializer.is_valid(raise_exception=True)

        logger.debug('REQUEST DATA: %s', request.data)

        instance = self.get_object()
        instance = GroupService().add_section(
            instance,
            **input_serializer.validated_data
        )

        output_serializer = GroupSerializer(
            instance, context={'request': request}
        )

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def _get_sections(self, request, uuid=None):
        """
        Returns Section instances associated with the given Group.
        """
        logger.debug('Searching for sections for group with uuid %s', uuid)

        instance = get_object_or_404(Group, uuid=uuid)
        instances = instance.sections.filter(hidden=False).distinct()

        logger.debug(
            'Found %s instance(s) that are not hidden', len(instances))

        if len(instances) == 0:
            logger.warn('No sections defined for group with uuid %s\
                - Did you forget to call setup ?', instance.uuid)

        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = SectionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = SectionSerializer(instances, many=True)
            return Response(serializer.data)

        return Response(output_serializer.data)

    @action(
        detail=True, methods=['get'], permission_classes=[IsAuthenticated],
        url_path='camps')
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: SectionSerializer},
    )
    def get_camps(self, request, uuid=None):
        """
        """
