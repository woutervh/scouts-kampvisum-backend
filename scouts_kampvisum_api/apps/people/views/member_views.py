import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from apps.people.serializers import InuitsMemberSerializer
from apps.people.filters import InuitsMemberFilter

from scouts_auth.groupadmin.services import GroupAdmin


logger = logging.getLogger(__name__)


class MemberViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = InuitsMemberFilter
    ordering_fields = ["id"]
    ordering = ["id"]

    service = GroupAdmin()

    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsMemberSerializer})
    def list(self, request):
        inuits_non_members = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(inuits_non_members)

        if page is not None:
            serializer = InuitsMemberSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = InuitsMemberSerializer(inuits_non_members, many=True)
            return Response(serializer.data)
