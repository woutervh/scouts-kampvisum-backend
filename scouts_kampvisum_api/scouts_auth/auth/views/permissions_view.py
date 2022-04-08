from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg2.utils import swagger_auto_schema

from scouts_auth.auth.models import User

from scouts_auth.groupadmin.models import ScoutsGroup
from scouts_auth.groupadmin.services import ScoutsAuthorizationService


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class PermissionsViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    authorization_service = ScoutsAuthorizationService()

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializers.Serializer})
    def get(self, request):
        try:
            user: User = request.user

            return Response(user.permissions)
        except Exception as exc:
            logger.error("SCOUTS_AUTH: Error while getting user permissions", exc)

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializers.Serializer})
    def get_for_group(self, request, group_admin_id: str):
        try:
            user: User = request.user
            group: ScoutsGroup = ScoutsGroup.objects.safe_get(
                group_admin_id=group_admin_id, raise_error=True
            )

            # HACKETY HACK
            # This should probably be handled by a rest call when changing groups in the frontend,
            # but adding it here avoids the need for changes to the frontend
            self.authorization_service.update_user_authorizations(
                user=request.user, scouts_group=group
            )

            return Response(user.permissions)
        except Exception as exc:
            logger.error("SCOUTS_AUTH: Error while getting user permissions", exc)
