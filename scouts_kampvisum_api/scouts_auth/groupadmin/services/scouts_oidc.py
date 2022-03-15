import jwt

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

from scouts_auth.auth.oidc import InuitsOIDCAuthenticationBackend
from scouts_auth.auth.signals import ScoutsAuthSignalSender
from scouts_auth.auth.settings import OIDCSettings

from scouts_auth.groupadmin.models import AbstractScoutsMember, ScoutsUser
from scouts_auth.groupadmin.serializers import AbstractScoutsMemberSerializer
from scouts_auth.groupadmin.services import GroupAdmin, ScoutsAuthorizationService


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsOIDCAuthenticationBackend(InuitsOIDCAuthenticationBackend):
    service = GroupAdmin()
    authorization_service = ScoutsAuthorizationService()
    signal_sender = ScoutsAuthSignalSender()

    def create_user(self, claims: dict) -> settings.AUTH_USER_MODEL:
        """
        Create and return a new user object.
        """
        username = None
        access_token = claims.get("access_token", None)
        if access_token:
            try:
                decoded = jwt.decode(
                    access_token,
                    algorithms=["RS256"],
                    verify=False,
                    options={"verify_signature": False},
                )
                username = decoded.get("preferred_username", None)
            except:
                logger.error("Unable to decode JWT token - Do you need a refresh ?")
        username = username if username else member.username
        # logger.debug("USER: create user %s", username)

        member: AbstractScoutsMember = self._load_member_data(data=claims)
        user: settings.AUTH_USER_MODEL = self.UserModel.objects.create_user(
            username=username, email=member.email
        )
        user = self._merge_member_data(user, member, claims)

        logger.debug(
            "SCOUTS OIDC AUTHENTICATION: Created a user with username %s from member %s",
            user.username,
            member.group_admin_id,
        )
        self.signal_sender.send_oidc_login(user=user)

        return user

    def update_user(
        self, user: settings.AUTH_USER_MODEL, claims: dict
    ) -> settings.AUTH_USER_MODEL:
        """
        Update existing user with new claims if necessary, save, and return the updated user object.
        """
        # logger.debug("USER: update user")

        member: AbstractScoutsMember = self._load_member_data(data=claims)
        user: settings.AUTH_USER_MODEL = self._merge_member_data(user, member, claims)

        user.last_refreshed = timezone.now()
        user.full_clean()
        user.save()

        logger.debug(
            "SCOUTS OIDC AUTHENTICATION: Updated a user with username %s ",
            user.username,
        )
        self.signal_sender.send_oidc_refresh(user=user)

        return user

    def _load_member_data(self, data: dict) -> AbstractScoutsMember:
        serializer = AbstractScoutsMemberSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        member: AbstractScoutsMember = serializer.save()

        return member

    def _merge_member_data(
        self, user: settings.AUTH_USER_MODEL, member: AbstractScoutsMember, claims: dict
    ) -> settings.AUTH_USER_MODEL:
        user: ScoutsUser = ScoutsUser.from_abstract_member(
            user=user, abstract_member=member
        )

        user.access_token = claims.get("access_token")
        user = self.map_user_with_claims(user=user)

        user.full_clean()
        user.save()

        return user

    def map_user_with_claims(
        self, user: settings.AUTH_USER_MODEL, claims: dict = None
    ) -> settings.AUTH_USER_MODEL:
        """
        Override the mapping in InuitsOIDCAuthenticationBackend to handle scouts-specific data.
        """
        logger.debug("SCOUTS OIDC AUTHENTICATION: mapping user with claims")
        return self.authorization_service.update_user_authorizations(user=user)
