from rest_framework import views, permissions, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from scouts_auth.auth.models import User
from scouts_auth.auth.serializers import UserSerializer

from scouts_auth.groupadmin.services import GroupAdmin


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class PermissionsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    service = GroupAdmin()

    @swagger_auto_schema(responses={status.HTTP_200_OK: UserSerializer})
    def get(self, request):
        try:
            user: User = request.user

            return Response(user.permissions)
        except Exception as exc:
            logger.error("SCOUTS_AUTH: Error while getting user permissions", exc)
