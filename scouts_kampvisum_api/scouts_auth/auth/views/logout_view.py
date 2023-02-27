from rest_framework import views, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from scouts_auth.scouts.services import ScoutsUserSessionService


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class LogoutView(views.APIView):

    service = ScoutsUserSessionService()

    @swagger_auto_schema(responses={status.HTTP_200_OK})
    def get(self, request):
        logger.debug(f"LOGOUT", user=request.user)

        self.service.remove_user_from_session(request.user.username)

        return Response(f'[{request.user.username}] LOGGED OUT')
