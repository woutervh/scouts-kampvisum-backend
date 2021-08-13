import logging
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from .models import ScoutsGroup
from .serializers import ScoutsGroupSerializer
from ....groupadmin.services import GroupAdminService


logger = logging.getLogger(__name__)


class ScoutsGroupViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing scout groups for the current user.
    """
    
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
    
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: ScoutsGroupSerializer}
    )
    def list(self, request):
        """
        Retrieves a list of all existing ScoutsSectionName instances.
        """
        
        user = request.user
        
        logger.info('USER: %s', user)
        
        groups = user.scouts_groups
        logger.info('GROUPS: %s', groups)
        instances = GroupAdminService().get_groups(groups)
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = ScoutsGroupSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = ScoutsGroupSerializer(instances, many=True)
            return Response(serializer.data)

