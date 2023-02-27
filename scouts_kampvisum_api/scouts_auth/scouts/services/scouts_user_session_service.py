
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
    def get_user_from_session(access_token: ScoutsToken) -> settings.AUTH_USER_MODEL:
        session: ScoutsUserSession = ScoutsUserSession.from_session(
            username=access_token.preferred_username)
        if session:
            logger.debug(
                f"[{access_token.preferred_username}] USER SESSION - Retrieving user from session")

            user = ScoutsUser.objects.safe_get(
                username=access_token.preferred_username, raise_error=True)

            deserialized = ScoutsUserSessionSerializer.to_scouts_user(
                session=session)

            # Clear any lingering data
            user.clear_data()

            for scouts_group in deserialized["scouts_groups"]:
                user.add_scouts_group(scouts_group)
            for scouts_function in deserialized["scouts_functions"]:
                user.add_scouts_function(scouts_function)

            user.access_token = access_token

            return user
        return None

    @staticmethod
    def store_user_in_session(access_token: ScoutsToken, scouts_user: settings.AUTH_USER_MODEL) -> ScoutsUserSession:
        logger.debug(f"USER SESSION - Storing user in session",
                     user=scouts_user)

        if access_token.preferred_username != scouts_user.username:
            raise ScoutsAuthException(
                f"Username in token ({access_token.preferred_username}) does not equal user's username ({scouts_user.username})")

        session = ScoutsUserSession.from_session(
            username=access_token.preferred_username)

        if not session:
            session = ScoutsUserSession()

        session.username = access_token.preferred_username
        session.expiration = access_token.exp
        session.data = ScoutsUserSessionSerializer.to_user_session(
            scouts_user=scouts_user)

        session.full_clean()
        session.save()

        return session
