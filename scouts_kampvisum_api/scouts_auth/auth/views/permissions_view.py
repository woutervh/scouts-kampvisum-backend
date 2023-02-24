from django.conf import settings
from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg2.utils import swagger_auto_schema

from scouts_auth.auth.models import User

from scouts_auth.groupadmin.models import ScoutsUser, ScoutsGroup
from scouts_auth.scouts.services import ScoutsPermissionService


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class PermissionsViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    authorization_service = ScoutsPermissionService()

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializers.Serializer})
    def get(self, request):
        try:
            user: settings.AUTH_USER_MODEL = request.user

            return Response(user.permissions)
        except Exception as exc:
            logger.error(
                "SCOUTS_AUTH: Error while getting user permissions", exc)
