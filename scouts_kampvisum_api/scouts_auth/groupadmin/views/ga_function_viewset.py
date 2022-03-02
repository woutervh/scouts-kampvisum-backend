from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema

from scouts_auth.groupadmin.models import (
    AbstractScoutsFunctionListResponse,
    AbstractScoutsFunction,
)
from scouts_auth.groupadmin.serializers import (
    AbstractScoutsFunctionListResponseSerializer,
    AbstractScoutsFunctionSerializer,
)
from scouts_auth.groupadmin.services import GroupAdmin


import logging

logger = logging.getLogger(__name__)


class AbstractScoutsFunctionView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    service = GroupAdmin()

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: AbstractScoutsFunctionListResponseSerializer}
    )
    @action(
        methods=["GET"],
        url_path="",
        detail=False,
    )
    def view_functions(self, request) -> Response:
        logger.debug("GA: Received request for a list of all functions")

        functions_response: AbstractScoutsFunctionListResponse = (
            self.service.get_functions(request.user)
        )
        serializer = AbstractScoutsFunctionListResponseSerializer(functions_response)

        return Response(serializer.data)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: AbstractScoutsFunctionListResponseSerializer}
    )
    @action(
        methods=["GET"],
        url_path=r"group/(?P<group_group_admin_id_fragment>\w+)",
        detail=False,
    )
    def view_function_list(
        self, request, group_group_admin_id_fragment: str
    ) -> Response:
        logger.debug(
            "GA: Received request for list of functions (group_group_admin_id_fragment: %s)",
            group_group_admin_id_fragment,
        )

        functions_response: AbstractScoutsFunctionListResponse = (
            self.service.get_functions(request.user, group_group_admin_id_fragment)
        )

        serializer = AbstractScoutsFunctionListResponseSerializer(functions_response)

        return Response(serializer.data)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: AbstractScoutsFunctionSerializer}
    )
    @action(
        methods=["GET"],
        url_path=r"(?P<function_id>\w+)",
        detail=True,
    )
    def view_function(self, request, function_id: str) -> Response:
        logger.debug(
            "GA: Received request for function info (function_id: %s)", function_id
        )

        function: AbstractScoutsFunction = self.service.get_function(
            request.user, function_id
        )

        serializer = AbstractScoutsFunctionSerializer(function)

        return Response(serializer.data)
