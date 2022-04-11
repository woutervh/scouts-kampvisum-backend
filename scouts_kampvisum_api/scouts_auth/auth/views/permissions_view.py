from django.conf import settings
from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg2.utils import swagger_auto_schema

from scouts_auth.auth.models import User

from scouts_auth.groupadmin.models import ScoutsUser, ScoutsGroup
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
            user: settings.AUTH_USER_MODEL = request.user

            return Response(user.permissions)
        except Exception as exc:
            logger.error("SCOUTS_AUTH: Error while getting user permissions", exc)

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializers.Serializer})
    def get_for_group(self, request, group_admin_id: str):
        try:
            user: settings.AUTH_USER_MODEL = request.user
            group: ScoutsGroup = ScoutsGroup.objects.safe_get(
                group_admin_id=group_admin_id, raise_error=True
            )

            # HACKETY HACK
            # This should probably be handled by a rest call when changing groups in the frontend,
            # but adding it here avoids the need for changes to the frontend
            user: settings.AUTH_USER_MODEL = (
                self.authorization_service.update_user_authorizations(
                    user=request.user, scouts_group=group
                )
            )

            user: settings.AUTH_USER_MODEL = ScoutsUser.objects.get(pk=user.pk)

            return Response(user.permissions)
        except Exception as exc:
            logger.error("SCOUTS_AUTH: Error while getting user permissions", exc)
