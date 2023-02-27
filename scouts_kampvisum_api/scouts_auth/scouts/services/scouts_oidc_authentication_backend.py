from typing import List
from types import SimpleNamespace

from django.conf import settings
from django.utils import timezone

from scouts_auth.auth.oidc import InuitsOIDCAuthenticationBackend
from scouts_auth.groupadmin.models import AbstractScoutsMember, ScoutsUser, ScoutsToken
from scouts_auth.groupadmin.services import GroupAdmin
from scouts_auth.groupadmin.serializers import AbstractScoutsMemberSerializer
from scouts_auth.scouts.services import ScoutsUserService, ScoutsUserSessionService


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
        if access_token:
            token: ScoutsToken = ScoutsToken.from_access_token(
                access_token=access_token)
            # self.groupadmin.ping(active_user=SimpleNamespace(username=token.preferred_username, access_token=token.access_token)

        user: settings.AUTH_USER_MODEL = ScoutsUserSessionService.get_user_from_session(
            access_token=token)
        if user:
            return user

        claims = self.get_userinfo(token, id_token, payload)

        users: List[settings.AUTH_USER_MODEL] = self.filter_users_by_claims(
            claims=claims, access_token=token)

        user_count = len(users)
        if user_count == 1:
            return self.update_user(user=users[0], claims=claims, access_token=token)
        elif user_count > 1:
            raise ValidationError(f"Multiple users returned: {user_count}")
        elif self.get_settings("OIDC_CREATE_USER", True):
            return self.create_user(claims=claims, access_token=token)
        else:
            raise ScoutsAuthException(
                f"Login failed: No user with {self.describe_user_by_claims(claims)} found, and OIDC_CREATE_USER is False",
            )

    def get_userinfo(self, access_token: ScoutsToken, id_token, payload) -> dict:
        """
        Return user details dictionary. The id_token and payload are not used
        in the default implementation, but may be used when overriding
        this method.
        """
        # Don't deserialise yet
        result = self.groupadmin.get_member_profile_raw(
            active_user=SimpleNamespace(
                username=access_token.preferred_username, access_token=access_token.access_token)
        )

        # Add token to user response so we can access it later
        result["access_token"] = access_token

        return result

    def filter_users_by_claims(self, claims: dict, access_token: ScoutsToken) -> List[settings.AUTH_USER_MODEL]:
        """
        Returns all users matching the group admin id or username (from claims or jwt).
        """

        # From group admin id in claims
        group_admin_id = claims.get("id", None)
        if group_admin_id:
            return self.UserModel.objects.filter(pk=group_admin_id)

        # From username "username" or "gebruikersnaam" in claims or from jwt
        username = self.get_username(
            claims=claims, access_token=access_token)
        if username:
            return self.UserModel.objects.filter(username=username)

        return []

    def get_username(self, claims: dict, access_token: ScoutsToken) -> str:
        """
        Gets the username from any of the provided or configured data
        """
        if GroupAdminSettings.get_username_from_access_token():
            return access_token.preferred_username

        if "username" in claims:
            return claims["username"]

        if "preferred_username" in claims:
            return claims["preferred_username"]

        if "gebruikersnaam" in claims:
            return claims["gebruikersnaam"]

        raise ScoutsAuthException(
            "Unable to get a username from jwt access token or claims (tried keys: 'username', 'preferred_username', 'gebruikersnaam'")

    def create_user(self, claims: dict, access_token: ScoutsToken = None) -> settings.AUTH_USER_MODEL:
        """
        Create and return a new user object.
        """

        member: AbstractScoutsMember = self._deserialize_member_data(
            claims=claims)
        user: settings.AUTH_USER_MODEL = self.UserModel.objects.create_user(
            id=member.group_admin_id, username=member.username, email=member.email
        )
        user = self._merge_member_data(
            user=user, member=member, claims=claims, access_token=access_token)

        logger.info(
            f"SCOUTS OIDC AUTHENTICATION: Created user from group admin member {member.group_admin_id}",
            user=user,
        )

        return user

    def update_user(
        self, user: settings.AUTH_USER_MODEL, claims: dict, access_token: ScoutsToken = None
    ) -> settings.AUTH_USER_MODEL:
        """
        Update existing user with new claims if necessary, save, and return the updated user object.
        """
        member: AbstractScoutsMember = self._deserialize_member_data(
            claims=claims)
        user: settings.AUTH_USER_MODEL = self._merge_member_data(
            user=user, member=member, claims=claims, access_token=access_token)

        logger.info(
            "SCOUTS OIDC AUTHENTICATION: Updated user",
            user=user,
        )

        return user

    def _deserialize_member_data(self, claims: dict) -> AbstractScoutsMember:
        """
        Serialises the raw user info from GroepsAdmin into an AbstractScoutsMember object.
        """

        serializer = AbstractScoutsMemberSerializer(data=claims)
        serializer.is_valid(raise_exception=True)

        return serializer.save()

    def _merge_member_data(
        self, user: settings.AUTH_USER_MODEL, member: AbstractScoutsMember, claims: dict, access_token: ScoutsToken = None
    ) -> settings.AUTH_USER_MODEL:
        """
        Persists the AbstractScoutsMember into a ScoutsUser object.
        """

        user = ScoutsUser.from_abstract_member(
            user=user, abstract_member=member)

        user.access_token = access_token if access_token else claims.get(
            "access_token")

        user.is_staff = True
        user.updated_on = timezone.now()

        user.full_clean()
        user.save()

        user: settings.AUTH_USER_MODEL = self.user_service.get_scouts_user(
            active_user=user, abstract_member=member)

        ScoutsUserSessionService.store_user_in_session(
            access_token=access_token, scouts_user=user)

        return user

    def authenticate(self, request):
        logger.warn(
            f"Self-authenticating through backend, should be through OIDCInuitsAuthentication", user=request.user)
