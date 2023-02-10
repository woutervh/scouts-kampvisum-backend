from typing import List
from types import SimpleNamespace

from django.conf import settings
from django.utils import timezone

from scouts_auth.auth.oidc import InuitsOIDCAuthenticationBackend

from scouts_auth.groupadmin.models import AbstractScoutsMember, ScoutsUser
from scouts_auth.groupadmin.services import GroupAdmin
from scouts_auth.groupadmin.serializers import AbstractScoutsMemberSerializer

from scouts_auth.scouts.services import ScoutsUserService


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsOIDCAuthenticationBackend(InuitsOIDCAuthenticationBackend):

    groupadmin = GroupAdmin()
    user_service = ScoutsUserService()

    def has_perm(self, user_obj, perm, obj=None) -> bool:
        result = super().has_perm(user_obj, perm, obj)

        # logger.debug(
        #     f"SCOUTS OIDC AUTHENTICATION BACKEND: has_perm: {result}, user_obj -> {user_obj.username}, perm -> {perm}, obj -> {obj}")

        return result

    # This is the method that's called by DRF's OIDCAuthentication (in the authenticate() method),
    # subclassed in InuitsOIDCAuthentication.
    def get_or_create_user(self, access_token, id_token, payload) -> settings.AUTH_USER_MODEL:
        """
        Returns a User instance if 1 user is found. Creates a user if not found
        and configured to do so. Returns nothing if multiple users are matched.
        """
        user_info = self.get_userinfo(access_token, id_token, payload)

        users: List[settings.AUTH_USER_MODEL] = self.filter_users_by_user_info(
            user_info=user_info, access_token=access_token)

        user_count = len(users)
        if user_count == 1:
            return self.update_user(user=users[0], user_info=user_info)
        elif user_count > 1:
            raise ValidationError(f"Multiple users returned: {user_count}")
        elif self.get_settings("OIDC_CREATE_USER", True):
            return self.create_user(user_info=user_info)
        else:
            raise ScoutsAuthException(
                f"Login failed: No user with {self.describe_user_by_user_info(user_info)} found, and OIDC_CREATE_USER is False",
            )

    def get_userinfo(self, access_token, id_token, payload) -> dict:
        """
        Return user details dictionary. The id_token and payload are not used
        in the default implementation, but may be used when overriding
        this method.
        """
        # Don't deserialise yet
        result = self.groupadmin.get_member_profile_raw(
            active_user=SimpleNamespace(access_token=access_token)
        )

        # Add token to user response so we can access it later
        result["access_token"] = access_token

        return result

    def filter_users_by_user_info(self, user_info: dict, access_token: str) -> List[settings.AUTH_USER_MODEL]:
        """
        Returns all users matching the group admin id or username (from user_info or jwt).
        """

        # From group admin id in user_info
        group_admin_id = user_info.get("id", None)
        if group_admin_id:
            return self.UserModel.objects.filter(pk=group_admin_id)

        # From username "username" or "gebruikersnaam" in user_info or from jwt
        username = self.get_username(
            user_info=user_info, access_token=access_token)
        if username:
            return self.UserModel.objects.filter(username=username)

        return []

    def get_username(self, user_info: dict, access_token: str) -> str:
        """
        Gets the username from any of the provided or configured data
        """
        if GroupAdminSettings.get_username_from_access_token():
            return self.get_username_from_access_token(access_token)

        if "username" in user_info:
            return user_info["username"]

        if "preferred_username" in user_info:
            return user_info["preferred_username"]

        if "gebruikersnaam" in user_info:
            return user_info["gebruikersnaam"]

        raise ScoutsAuthException(
            "Unable to get a username from jwt access token or user_info (tried keys: 'username', 'preferred_username', 'gebruikersnaam'")

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
            except Exception as exc:
                raise ScoutsAuthException(
                    "Unable to decode JWT token - Do you need a refresh ?", cause=exc)

        raise ScoutsAuthException(
            "Unable to retrieve username from JWT access token")

    def create_user(self, user_info: dict) -> settings.AUTH_USER_MODEL:
        """
        Create and return a new user object.
        """

        member: AbstractScoutsMember = self._deserialize_member_data(
            user_info=user_info)
        user: settings.AUTH_USER_MODEL = self.UserModel.objects.create_user(
            id=member.group_admin_id, username=member.username, email=member.email
        )
        user = self._merge_member_data(
            user=user, member=member, user_info=user_info)

        logger.info(
            f"SCOUTS OIDC AUTHENTICATION: Created user from group admin member {member.group_admin_id}",
            user=user,
        )

        return user

    def update_user(
        self, user: settings.AUTH_USER_MODEL, user_info: dict
    ) -> settings.AUTH_USER_MODEL:
        """
        Update existing user with new user_info if necessary, save, and return the updated user object.
        """

        member: AbstractScoutsMember = self._deserialize_member_data(
            user_info=user_info)
        user: settings.AUTH_USER_MODEL = self._merge_member_data(
            user=user, member=member, user_info=user_info)

        logger.info(
            "SCOUTS OIDC AUTHENTICATION: Updated user",
            user=user,
        )

        return user

    def _deserialize_member_data(self, user_info: dict) -> AbstractScoutsMember:
        """
        Serialises the raw user info from GroepsAdmin into an AbstractScoutsMember object.
        """

        serializer = AbstractScoutsMemberSerializer(data=user_info)
        serializer.is_valid(raise_exception=True)

        return serializer.save()

    def _merge_member_data(
        self, user: settings.AUTH_USER_MODEL, member: AbstractScoutsMember, user_info: dict
    ) -> settings.AUTH_USER_MODEL:
        """
        Persists the AbstractScoutsMember into a ScoutsUser object.
        """

        user = ScoutsUser.from_abstract_member(
            user=user, abstract_member=member)

        user.access_token = user_info.get("access_token")

        user.is_staff = True
        user.updated_on = timezone.now()

        user.full_clean()
        user.save()

        return self.user_service.get_scouts_user(active_user=user, abstract_member=member)

    def authenticate(self, request):
        logger.warn(
            f"Self-authenticating through backend, should be through OIDCInuitsAuthentication", user=request.user)
