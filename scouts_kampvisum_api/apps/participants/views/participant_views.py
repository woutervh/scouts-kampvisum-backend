from typing import List

from django.conf import settings
from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema

from apps.participants.models import InuitsParticipant
from apps.participants.models.enums import ParticipantType
from apps.participants.serializers import InuitsParticipantSerializer
from apps.participants.filters import InuitsParticipantFilter
from apps.participants.services import InuitsParticipantService
from apps.participants.pagination import InuitsParticipantPagination

from apps.visums.models import LinkedCheck, LinkedParticipantCheck

from scouts_auth.groupadmin.models import AbstractScoutsMember
from scouts_auth.groupadmin.services import GroupAdminMemberService
from scouts_auth.groupadmin.settings import GroupAdminSettings

from scouts_auth.scouts.permissions import ScoutsFunctionPermissions


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ParticipantViewSet(viewsets.GenericViewSet):

    serializer_class = InuitsParticipantSerializer
    queryset = InuitsParticipant.objects.all()
    permission_classes = (ScoutsFunctionPermissions, )
    pagination_class = InuitsParticipantPagination
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = InuitsParticipantFilter
    ordering_fields = ["id"]
    ordering = ["id"]

    participant_service = InuitsParticipantService()
    groupadmin = GroupAdminMemberService()

    @swagger_auto_schema(
        request_body=InuitsParticipantSerializer,
        responses={status.HTTP_201_CREATED: InuitsParticipantSerializer},
    )
    def create(self, request):
        # logger.debug("PARTICIPANT CREATE REQUEST DATA: %s", request.data)
        input_serializer = InuitsParticipantSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug(
            "PARTICIPANT CREATE VALIDATED REQUEST DATA: %s", validated_data)

        participant = self.participant_service.create_or_update_participant(
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
        logger.debug("PARTICIPANT: %s", self.get_object())
        logger.debug(
            "PARTICIPANT PARTIAL UPDATE REQUEST DATA: %s", request.data)
        serializer = InuitsParticipantSerializer(
            instance=participant,
            data=request.data,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug(
            "PARTICIPANT PARTIAL UPDATE VALIDATED DATA: %s", validated_data)

        participant = self.participant_service.update(
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
            include_inactive=GroupAdminSettings.include_inactive_members_in_search(),
        )

    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsParticipantSerializer})
    def list_participants(self, request):
        queryset = self.get_queryset()
        participants = self.filter_queryset(queryset)

        output_serializer = InuitsParticipantSerializer(
            participants, many=True)

        return Response(output_serializer.data)

    @action(methods=["get"], detail=False)
    def list_scouts_members(self, request):
        return self._list(request=request, only_scouts_members=True)

    @action(methods=["get"], detail=False)
    def list_scouts_members_all(self, request):
        return self._list(request=request, only_scouts_members=True, all_members=True)

    def _list(self, request, include_inactive: bool = False, only_scouts_members=False, all_members=False):
        check = self.request.GET.get("check", None)
        search_term = self.request.GET.get("term", None)
        group_group_admin_id = self.request.GET.get("group", None)
        min_age = self.request.GET.get("min_age", None)
        max_age = self.request.GET.get("max_age", None)
        gender = self.request.GET.get("gender", None)
        participant_type = self.request.GET.get("type", None)

        if not (
            check
            or search_term
            or group_group_admin_id
            or min_age
            or max_age
            or gender
            or participant_type
        ):
            if only_scouts_members:
                return Response({})
            else:
                return self.list_participants(request)

        if not search_term and not all_members:
            raise ValidationError("Url param 'term' is a required filter")

        if participant_type:
            type = ParticipantType.parse_participant_type(participant_type)

            if not type:
                raise ValidationError(
                    "Unknown ParticipantType {}".format(participant_type)
                )

            participant_type = type

        if check:
            check: LinkedParticipantCheck = LinkedCheck.get_concrete_check_type_by_id(
                check
            )

            participant_type = check.participant_check_type

        # Ticket #90610 https://redmine.inuits.eu/issues/90610
        presets = {}
        if participant_type:
            presets["participant_type"] = participant_type
            presets["include_inactive"] = False
            presets["leader"] = True
            presets["active_leader"] = False
            presets["only_scouts_members"] = True

            if ParticipantType.is_member(participant_type):
                presets["leader"] = False
            elif ParticipantType.is_cook(participant_type):
                presets["leader"] = True
                presets["include_inactive"] = True

            elif ParticipantType.is_leader(participant_type):
                presets["active_leader"] = True

            elif ParticipantType.is_responsible(participant_type):
                presets["active_leader"] = True

            elif ParticipantType.is_adult(participant_type):
                presets["leader"] = True
                presets["include_inactive"] = True
                presets["min_age"] = GroupAdminSettings.get_camp_responsible_min_age()

            if presets.get("active_leader", False) and not group_group_admin_id:
                raise ValidationError(
                    "Can only search for active leaders in a group, no group admin id given"
                )

            include_inactive = presets.get(
                "include_inactive", include_inactive)
            only_scouts_members = presets.get(
                "only_scouts_members", only_scouts_members
            )

        logger.debug(
            "Searching for %s with additional parameters: group_group_admin_id(%s), min_age(%s), max_age(%s), gender(%s), include_inactive (%s), only_scouts_members(%s) and presets (%s)",
            search_term,
            group_group_admin_id,
            min_age,
            max_age,
            gender,
            include_inactive,
            only_scouts_members,
            presets,
        )

        # search_term = (
        #     "{} {}".format(search_term, "|")
        #     if search_term.strip()[-1] != "|"
        #     else search_term
        # )
        if all_members:
            members: List[AbstractScoutsMember] = self.groupadmin.search_member_filtered_all(
                active_user=request.user,
                term=search_term,
                group_group_admin_id=group_group_admin_id,
                min_age=min_age,
                max_age=max_age,
                gender=gender,
            )
        else:
            members: List[AbstractScoutsMember] = self.groupadmin.search_member_filtered(
                active_user=request.user,
                term=search_term,
                group_group_admin_id=group_group_admin_id,
                min_age=min_age,
                max_age=max_age,
                gender=gender,
                include_inactive=include_inactive,
                presets=presets,
            )
        members = sorted(members, key=lambda x: (x.first_name, x.last_name))

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

        if page is None or all_members:
            serializer = InuitsParticipantSerializer(
                results, many=True, context={"request": request}
            )
            return Response(serializer.data)
        else:
            serializer = InuitsParticipantSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)
