import jwt

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

from scouts_auth.auth.oidc import InuitsOIDCAuthenticationBackend

from scouts_auth.groupadmin.models import AbstractScoutsMember, ScoutsUser
from scouts_auth.groupadmin.serializers import AbstractScoutsMemberSerializer
from scouts_auth.groupadmin.services import (
    GroupAdmin,
    ScoutsUserService,
    ScoutsAuthorizationService,
)


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsOIDCAuthenticationBackend(InuitsOIDCAuthenticationBackend):
    service = GroupAdmin()
    scouts_user_service = ScoutsUserService()
    authorization_service = ScoutsAuthorizationService()

    def get_userinfo(self, access_token, id_token, payload) -> dict:
        """
        Return user details dictionary. The id_token and payload are not used
        in the default implementation, but may be used when overriding
        this method.
        """

        now = timezone.now()
        logger.debug("SCOUTS OIDC AUTHENTICATION: requesting user info (%s)", now)
        result = super().get_userinfo(access_token, id_token, payload)
        after = timezone.now()
        logger.debug("SCOUTS OIDC AUTHENTICATION: user info requested (%s)", after)
        logger.debug(
            "SCOUTS OIDC AUTHENTICATION: user info request took %s", after - now
        )

        return result

    def get_or_create_user(self, access_token, id_token, payload):
        """Returns a User instance if 1 user is found. Creates a user if not found
        and configured to do so. Returns nothing if multiple users are matched."""
        # logger.debug("")
        # logger.debug("")
        # logger.debug("")
        # logger.debug("")
        # logger.debug("")
        # logger.debug("")
        # logger.debug("")
        # logger.debug("GET OR CREATE USER")

        # # access_token = auth.split(" ")[1]
        # decoded = jwt.decode(
        #     access_token,
        #     algorithms=["RS256"],
        #     verify=False,
        #     options={"verify_signature": False},
        # )
        # username = decoded.get("preferred_username", None)
        # logger.debug("USERNAME: %s", username)

        # if username:
        #     logger.debug("SETTING USERNAME on request")
        #     user = ScoutsUser.objects.safe_get(username=username)

        #     if user:
        #         logger.debug("USER FOUND: %s", user.username)
        #         return user

        user_info = self.get_userinfo(access_token, id_token, payload)

        claims_verified = self.verify_claims(user_info)
        if not claims_verified:
            msg = "Claims verification failed"
            raise ValidationError(msg)

        # email based filtering
        users = self.filter_users_by_claims(user_info)

        logger.debug("GET OR CREATE USER FOUND %d user(s)", len(users))

        if len(users) == 1:
            return self.update_user(users[0], user_info)
        elif len(users) > 1:
            # In the rare case that two user accounts have the same email address,
            # bail. Randomly selecting one seems really wrong.
            msg = "Multiple users returned"
            raise ValidationError(msg)
        elif self.get_settings("OIDC_CREATE_USER", True):
            user = self.create_user(user_info)
            return user
        else:
            logger.debug(
                "Login failed: No user with %s found, and " "OIDC_CREATE_USER is False",
                self.describe_user_by_claims(user_info),
            )
            return None

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
        self.scouts_user_service.handle_oidc_login(user=user)

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

        logger.debug(
            "SCOUTS OIDC AUTHENTICATION: Updated a user with username %s ",
            user.username,
        )
        self.scouts_user_service.handle_oidc_refresh(user=user)

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
