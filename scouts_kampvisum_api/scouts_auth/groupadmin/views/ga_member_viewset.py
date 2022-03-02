from typing import List

from django.conf import settings

from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from drf_yasg2.utils import swagger_auto_schema

from scouts_auth.groupadmin.models import (
    AbstractScoutsGroupListResponse,
    AbstractScoutsMember,
    AbstractScoutsMemberListResponse,
)
from scouts_auth.groupadmin.serializers import (
    AbstractScoutsMemberSerializer,
    AbstractScoutsMemberFrontendSerializer,
    AbstractScoutsMemberSearchFrontendSerializer,
    AbstractScoutsMemberListResponseSerializer,
    ScoutsUserSerializer,
)
from scouts_auth.groupadmin.services import GroupAdminMemberService


import logging

logger = logging.getLogger(__name__)


class AbstractScoutsMemberView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    service = GroupAdminMemberService()

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: AbstractScoutsMemberListResponseSerializer}
    )
    @action(methods=["GET"], url_path="", detail=True)
    def view_member_list(self, request) -> Response:
        logger.debug("GA: Received request for member list")

        response: AbstractScoutsMemberListResponse = self.service.get_member_list(
            request.user
        )

        serializer = AbstractScoutsMemberListResponseSerializer(response)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: AbstractScoutsMemberSerializer})
    @action(
        methods=["GET"],
        url_path=r"(?P<group_admin_id>\w+)",
        detail=False,
    )
    def view_member_info_internal(self, request, group_admin_id: str) -> Response:
        logger.debug(
            "GA: Received request for member info (group_admin_id: %s)", group_admin_id
        )

        member: AbstractScoutsMember = self.service.get_member_info(
            request.user, group_admin_id
        )

        serializer = AbstractScoutsMemberSerializer(member)

        return Response(serializer.data)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: AbstractScoutsMemberFrontendSerializer}
    )
    @action(
        methods=["GET"],
        url_path=r"(?P<group_admin_id>\w+)",
        detail=False,
    )
    def view_member_info(self, request, group_admin_id: str) -> Response:
        logger.debug(
            "GA: Received request for member info (group_admin_id: %s)", group_admin_id
        )

        member: AbstractScoutsMember = self.service.get_member_info(
            request.user, group_admin_id
        )

        serializer = AbstractScoutsMemberFrontendSerializer(member)

        return Response(serializer.to_representation(member))

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: AbstractScoutsMemberListResponseSerializer}
    )
    @action(
        methods=["GET"],
        url_path=r"(?:/(?P<term>\w+))?(?:/(?P<group_group_admin_id>\w+))?",
        detail=True,
    )
    def search_members(
        self, request, term: str, group_group_admin_id: str = None
    ) -> Response:
        logger.debug("GA: Received request to search for members")
        logger.debug(
            "GA: Member search parameters: term(%s) - group_group_admin_id(%s)",
            term if term else "",
            group_group_admin_id if group_group_admin_id else "",
        )

        if not term:
            raise ValidationError("Url param 'term' is a required filter")

        results: List[AbstractScoutsMember] = self.service.search_member_filtered(
            request.user, term=term, group_group_admin_id=group_group_admin_id
        )

        serializer = AbstractScoutsMemberSearchFrontendSerializer(results, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: AbstractScoutsMemberSerializer})
    @action(
        methods=["GET"],
        url_path="",
        detail=True,
    )
    def view_member_profile_internal(self, request) -> Response:
        logger.debug("GA: Received request for current user GA member profile")

        member: AbstractScoutsMember = self.service.get_member_profile(request.user)

        serializer = AbstractScoutsMemberSerializer(member)

        return Response(serializer.data)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: AbstractScoutsMemberFrontendSerializer}
    )
    @action(
        methods=["GET"],
        url_path="",
        detail=True,
    )
    def view_member_profile(self, request) -> Response:
        logger.debug("GA: Received request for current user GA member profile")

        member: AbstractScoutsMember = self.service.get_member_profile(request.user)
        groups_response: AbstractScoutsGroupListResponse = self.service.get_groups(
            request.user
        )

        member.scouts_groups = groups_response.scouts_groups

        serializer = AbstractScoutsMemberFrontendSerializer(member)

        return Response(serializer.to_representation(member))

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: AbstractScoutsMemberFrontendSerializer}
    )
    @action(
        methods=["GET"],
        url_path="",
        detail=True,
    )
    def view_user(self, request) -> Response:
        logger.debug("GA: Received request for current user profile")

        user: settings.AUTH_USER_MODEL = request.user

        serializer = ScoutsUserSerializer(user)

        return Response(serializer.data)
