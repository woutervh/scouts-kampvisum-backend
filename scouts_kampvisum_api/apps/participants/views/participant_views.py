import logging
from typing import List

from django.core.exceptions import ValidationError
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema

from apps.participants.models import InuitsParticipant
from apps.participants.serializers import InuitsParticipantSerializer
from apps.participants.filters import InuitsParticipantFilter
from apps.participants.services import InuitsParticipantService

from scouts_auth.groupadmin.models import AbstractScoutsMember
from scouts_auth.groupadmin.serializers import AbstractScoutsMemberSerializer

logger = logging.getLogger(__name__)


class ParticipantViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = InuitsParticipantFilter
    ordering_fields = ["id"]
    ordering = ["id"]

    service = InuitsParticipantService()

    def get_queryset(self):
        return InuitsParticipant.objects.all()

    @swagger_auto_schema(
        request_body=InuitsParticipantSerializer,
        responses={status.HTTP_201_CREATED: InuitsParticipantSerializer},
    )
    def create(self, request):
        logger.debug("PARTICIPANT CREATE REQUEST DATA: %s", request.data)
        input_serializer = InuitsParticipantSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("PARTICIPANT CREATE VALIDATED REQUEST DATA: %s", validated_data)

        non_member = self.service.create_or_update(
            inuits_non_member=validated_data, user=request.user
        )

        output_serializer = InuitsParticipantSerializer(
            non_member, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsParticipantSerializer})
    def retrieve(self, request, pk=None):
        type = self.get_object()
        serializer = InuitsParticipantSerializer(type)

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=InuitsParticipantSerializer,
        responses={status.HTTP_200_OK: InuitsParticipantSerializer},
    )
    def partial_update(self, request, pk=None):
        inuits_non_member = self.get_object()

        serializer = InuitsParticipantSerializer(
            instance=inuits_non_member,
            data=request.data,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        inuits_non_member = self.service.update(
            inuits_non_member=inuits_non_member,
            updated_inuits_non_member=serializer.validated_data,
            updated_by=request.user,
        )

        output_serializer = InuitsParticipantSerializer(inuits_non_member)

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsParticipantSerializer})
    def list(self, request):
        inuits_non_members = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(inuits_non_members)

        if page is not None:
            serializer = InuitsParticipantSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = InuitsParticipantSerializer(inuits_non_members, many=True)
            return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsParticipantSerializer})
    def list(self, request):
        return self._list(request=request)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: InuitsParticipantSerializer},
    )
    @action(methods=["get"], detail=False, url_path="/inactive")
    def list_with_previous_members(self, request):
        return self._list(request=request, include_inactive=True)

    def _list(self, request, include_inactive: bool = False):
        search_term = self.request.GET.get("term", None)
        group_group_admin_id = self.request.GET.get("group", None)

        if not search_term:
            raise ValidationError("Url param 'term' is a required filter")

        if not group_group_admin_id:
            logger.debug(
                "Searching for members and non-members with search term %s", search_term
            )
        else:
            logger.debug(
                "Searching for members and non-members with term %s and group %s",
                search_term,
                group_group_admin_id,
            )

        members: List[AbstractScoutsMember] = self.service.search_member_filtered(
            active_user=request.user,
            term=search_term,
            group_group_admin_id=group_group_admin_id,
        )

        queryset = self.get_queryset()
        non_members = self.filter_queryset(queryset)
        results = [*members, *non_members]
        output_serializer = InuitsParticipantSerializer(results, many=True)

        return Response(output_serializer.data)
