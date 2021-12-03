import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from .serializers import GroupAdminGroupSerializer
from .services import GroupAdminService


logger = logging.getLogger(__name__)


class GroupAdminGroupViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing scout groups for the current user.
    """

    serializer_class = GroupAdminGroupSerializer

    @swagger_auto_schema(responses={status.HTTP_200_OK: GroupAdminGroupSerializer})
    def list(self, request):
        """
        Lists authorized groups from GroupAdmin.
        """

        user = request.user

        instances = GroupAdminService().get_groups(user)
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = GroupAdminGroupSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = GroupAdminGroupSerializer(instances, many=True)
            return Response(serializer.data)
