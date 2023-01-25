from types import SimpleNamespace
from typing import List

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

from scouts_auth.auth.oidc import InuitsOIDCAuthenticationBackend

from scouts_auth.groupadmin.settings import GroupAdminSettings
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

    def get_user(self, *args, **kwargs):
        logger.debug("HERE HERE HERE")
        logger.debug(f"ARGS: {args}")
        logger.debug(f"KWARGS: {kwargs}")

    # This is the method that's called by DRF's OIDCAuthentication (in the authenticate() method),
    # subclassed in InuitsOIDCAuthentication.
    def get_or_create_user(self, access_token, id_token, payload) -> settings.AUTH_USER_MODEL:
        """
        Returns a User instance if 1 user is found. Creates a user if not found
        and configured to do so. Returns nothing if multiple users are matched.
        """
        username = self.get_username_from_access_token(access_token)

        user_info = self.get_userinfo(access_token, id_token, payload)

        users: List[settings.AUTH_USER_MODEL] = self.filter_users_by_claims(
            user_info)

        user_count = len(users)
        if user_count == 1:
            return self.update_user(users[0], user_info)
        elif user_count > 1:
            raise ValidationError(f"Multiple users returned: {user_count}")
        elif self.get_settings("OIDC_CREATE_USER", True):
            user = self.create_user(user_info)
            return user
        else:
            logger.debug(
                "Login failed: No user with %s found, and " "OIDC_CREATE_USER is False",
                self.describe_user_by_claims(user_info),
            )
            return None

    def get_userinfo(self, access_token, id_token, payload) -> dict:
        """
        Return user details dictionary. The id_token and payload are not used
        in the default implementation, but may be used when overriding
        this method.
        """

        # Don't deserialise yet
        result = self.service.get_member_profile_raw(
            active_user=SimpleNamespace(access_token=access_token)
        )

        # Add token to user response so we can access it later
        result["access_token"] = access_token
        result["username"] = self.get_username(
            claims=result, access_token=access_token)

        return result

    def get_username(self, claims: dict, access_token: str) -> str:
        """
        Gets the username from any of the provided or configured data
        """
        if GroupAdminSettings.get_username_from_access_token():
            return self.get_username_from_access_token(access_token)

        if "username" in claims:
            return claims["username"]

        if "preferred_username" in claims:
            return claims["preferred_username"]

        if "gebruikersnaam" in claims:
            return claims["gebruikersnaam"]

        return None

    def get_username_from_access_token(self, access_token) -> str:
        """
        Parses the username from the JWT access token if configured to
        do so (through the env variable USERNAME_FROM_ACCESS_TOKEN).
        """
        import jwt

        if access_token:
            try:
                decoded = jwt.decode(
                    access_token,
                    algorithms=["RS256"],
                    verify=False,
                    options={"verify_signature": False},
                )
                return decoded.get("preferred_username", None)
            except:
                logger.error(
                    "Unable to decode JWT token - Do you need a refresh ?")

        return None

    def filter_users_by_claims(self, claims) -> List[settings.AUTH_USER_MODEL]:
        """Return all users matching the group admin id."""
        group_admin_id = claims.get("id", None)
        if group_admin_id:
            return self.UserModel.objects.filter(group_admin_id=group_admin_id)

        username = claims.get("username", None)
        if username:
            return self.UserModel.objects.filter(username=username)

        return []

    def create_user(self, claims: dict) -> settings.AUTH_USER_MODEL:
        """
        Create and return a new user object.
        """
        username = None

        member: AbstractScoutsMember = self._load_member_data(data=claims)
        username = username if username else member.username
        user: settings.AUTH_USER_MODEL = self.UserModel.objects.create_user(
            id=member.group_admin_id, username=username, email=member.email
        )
        user = self._merge_member_data(user, member, claims)

        logger.info(
            "SCOUTS OIDC AUTHENTICATION: Created user from group admin member %s",
            member.group_admin_id,
            user=user,
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
        user: settings.AUTH_USER_MODEL = self._merge_member_data(
            user, member, claims)

        logger.info(
            "SCOUTS OIDC AUTHENTICATION: Updated user",
            user=user,
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

        user.is_staff = True

        user.full_clean()
        user.save()

        return user

    def map_user_with_claims(
        self, user: settings.AUTH_USER_MODEL, claims: dict = None
    ) -> settings.AUTH_USER_MODEL:
        """
        Override the mapping in InuitsOIDCAuthenticationBackend to handle scouts-specific data.
        """
        logger.debug(
            "SCOUTS OIDC AUTHENTICATION: mapping user claims", user=user)
        return self.authorization_service.update_user_authorizations(user=user)
