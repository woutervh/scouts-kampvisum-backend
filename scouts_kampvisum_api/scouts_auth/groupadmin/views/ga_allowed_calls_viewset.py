from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from scouts_auth.groupadmin.models import ScoutsAllowedCalls
from scouts_auth.groupadmin.serializers import ScoutsAllowedCallsSerializer
from scouts_auth.groupadmin.services import GroupAdmin


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsAllowedCallsView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    service = GroupAdmin()

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsAllowedCallsSerializer})
    @action(
        methods=["GET"],
        url_path="",
        detail=False,
    )
    def view_allowed_calls(self, request):
        logger.debug("GA: Received request to view authorized groups")

        response: ScoutsAllowedCalls = self.service.get_allowed_calls(request.user)

        serializer = ScoutsAllowedCallsSerializer(response)

        return Response(serializer.data)
