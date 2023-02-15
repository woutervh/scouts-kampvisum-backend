
from django.conf import settings

from scouts_auth.auth.settings import InuitsOIDCSettings
from scouts_auth.auth.exceptions import ScoutsAuthException
from scouts_auth.groupadmin.models import ScoutsUser, ScoutsUserSession, ScoutsToken
from scouts_auth.groupadmin.serializers import ScoutsUserSessionSerializer

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsUserSessionService:

    @staticmethod
    def remove_user_from_session(username: str):
        ScoutsUserSession.objects.remove_session_data(username=username)

    @staticmethod
    def get_user_from_session(access_token: str) -> settings.AUTH_USER_MODEL:
        token: ScoutsToken = ScoutsToken.from_access_token(
            access_token=access_token)

        session: ScoutsUserSession = ScoutsUserSession.objects.get_session_data(
            username=token.preferred_username, expiration=token.exp)
        if session:
            logger.debug(
                f"[{token.preferred_username}] USER SESSION - Retrieving user from session")

            # logger.debug(
            #     f"[{token.preferred_username}] SESSION DATA: {session}")

            user = ScoutsUser.objects.safe_get(
                username=token.preferred_username, raise_exception=True)

            deserialized = ScoutsUserSessionSerializer.to_scouts_user(
                session=session)

            for scouts_group in deserialized["scouts_groups"]:
                logger.debug(
                    f"ADDING GROUP {scouts_group.group_admin_id} to user obj", user=user)
                user.add_scouts_group(scouts_group)
            for scouts_function in deserialized["scouts_functions"]:
                user.add_scouts_function(scouts_function)

            user.access_token = access_token

            return user
        return None

    @staticmethod
    def store_user_in_session(access_token: str, scouts_user: settings.AUTH_USER_MODEL) -> ScoutsUserSession:
        logger.debug(f"USER SESSION - Storing user in session",
                     user=scouts_user)

        token: ScoutsToken = ScoutsToken.from_access_token(
            access_token=access_token)

        if token.preferred_username != scouts_user.username:
            raise ScoutsAuthException(
                f"Username in token ({token.preferred_username}) does not equal user's username ({scouts_user.username})")

        session = ScoutsUserSession.objects.safe_get(
            username=token.preferred_username)

        if not session:
            session = ScoutsUserSession()

        session.username = token.preferred_username
        session.expiration = token.exp
        session.data = ScoutsUserSessionSerializer.to_user_session(
            scouts_user=scouts_user)

        session.full_clean()
        session.save()

        return session
