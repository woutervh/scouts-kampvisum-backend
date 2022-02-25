import logging
from typing import List

from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema

from apps.participants.models import InuitsParticipant
from apps.participants.serializers import InuitsParticipantSerializer
from apps.participants.filters import InuitsParticipantFilter
from apps.participants.services import InuitsParticipantService

from apps.visums.models import LinkedCheck

from scouts_auth.groupadmin.models import AbstractScoutsMember
from scouts_auth.groupadmin.services import GroupAdminMemberService
from scouts_auth.groupadmin.settings import GroupadminSettings

logger = logging.getLogger(__name__)


class ParticipantViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = InuitsParticipantFilter
    ordering_fields = ["id"]
    ordering = ["id"]

    service = InuitsParticipantService()
    groupadmin = GroupAdminMemberService()

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

        participant = self.service.create_or_update(
            participant=validated_data, user=request.user
        )

        output_serializer = InuitsParticipantSerializer(
            participant, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsParticipantSerializer})
    def retrieve(self, request, pk=None):
        instance: InuitsParticipant = self.get_object()
        serializer = InuitsParticipantSerializer(instance)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsParticipantSerializer})
    def retrieve_scouts_member(self, request, group_admin_id):
        scouts_member = self.groupadmin.get_member_info(
            active_user=request.user, group_admin_id=group_admin_id
        )
        serializer = InuitsParticipantSerializer(
            InuitsParticipant.from_scouts_member(scouts_member)
        )

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=InuitsParticipantSerializer,
        responses={status.HTTP_200_OK: InuitsParticipantSerializer},
    )
    def partial_update(self, request, pk=None):
        participant = self.get_object()

        logger.debug("PARTICIPANT PARTIAL UPDATE REQUEST DATA: %s", request.data)
        serializer = InuitsParticipantSerializer(
            instance=participant,
            data=request.data,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("PARTICIPANT PARTIAL UPDATE VALIDATED DATA: %s", validated_data)

        participant = self.service.update(
            participant=participant,
            updated_participant=validated_data,
            updated_by=request.user,
        )

        output_serializer = InuitsParticipantSerializer(participant)

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsParticipantSerializer})
    def list(self, request):
        return self._list(
            request=request,
            include_inactive=GroupadminSettings.include_inactive_members_in_search(),
        )

    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsParticipantSerializer})
    def list_participants(self, request):
        queryset = self.get_queryset()
        participants = self.filter_queryset(queryset)

        output_serializer = InuitsParticipantSerializer(participants, many=True)

        return Response(output_serializer.data)

    @action(methods=["get"], detail=False)
    def list_scouts_members(self, request):
        return self._list(request=request, only_scouts_members=True)

    def _list(self, request, include_inactive: bool = False, only_scouts_members=False):
        check = self.request.GET.get("check", None)
        search_term = self.request.GET.get("term", None)
        group_group_admin_id = self.request.GET.get("group", None)
        min_age = self.request.GET.get("min_age", None)
        max_age = self.request.GET.get("max_age", None)
        gender = self.request.GET.get("gender", None)

        if not (
            check or search_term or group_group_admin_id or min_age or max_age or gender
        ):
            if only_scouts_members:
                return Response({})
            else:
                return self.list_participants(request)

        if not search_term:
            raise ValidationError("Url param 'term' is a required filter")

        as_members = "participants"
        if check:
            check: LinkedCheck = LinkedCheck.get_concrete_check_type_by_id(check)

            find_members = False
            find_cooks = False
            find_leaders = False
            find_responsibles = False
            find_adults = False

            if check.parent.check_type.is_participant_member_check():
                find_members = True
                as_members = "members"
            elif check.parent.check_type.is_participant_cook_check():
                find_cooks = True
                as_members = "cooks"
            elif check.parent.check_type.is_participant_leader_check():
                find_leaders = True
                as_members = "leaders"
            elif check.parent.check_type.is_participant_responsible_check():
                find_responsibles = True
                as_members = "responsibles"
            elif check.parent.check_type.is_participant_adult_check():
                find_adults = True
                as_members = "adults"

        logger.debug(
            "Searching for %s (as %s) with additional parameters: group_group_admin_id(%s), min_age(%s), max_age(%s), gender(%s), include_inactive (%s), only_scouts_members(%s)",
            search_term,
            as_members,
            group_group_admin_id,
            min_age,
            max_age,
            gender,
            include_inactive,
            only_scouts_members,
        )

        members: List[AbstractScoutsMember] = self.groupadmin.search_member_filtered(
            active_user=request.user,
            term=search_term,
            group_group_admin_id=group_group_admin_id,
            min_age=min_age,
            max_age=max_age,
            gender=gender,
            include_inactive=include_inactive,
        )

        if only_scouts_members:
            results = [
                InuitsParticipant.from_scouts_member(member) for member in members
            ]
        else:
            queryset = self.get_queryset().non_members()
            non_members = self.filter_queryset(queryset)
            logger.debug("%d NON MEMBERS", len(non_members))
            results = [
                *[InuitsParticipant.from_scouts_member(member) for member in members],
                *non_members,
            ]

        page = self.paginate_queryset(results)

        if page is not None:
            serializer = InuitsParticipantSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)
        else:
            serializer = InuitsParticipantSerializer(
                results, many=True, context={"request": request}
            )
            return Response(serializer.data)
