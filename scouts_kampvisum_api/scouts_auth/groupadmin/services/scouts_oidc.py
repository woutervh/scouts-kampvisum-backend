import jwt

from django.conf import settings
from django.core.exceptions import ValidationError

from scouts_auth.auth.oidc import InuitsOIDCAuthenticationBackend
from scouts_auth.auth.settings import OIDCSettings

from scouts_auth.groupadmin.models import AbstractScoutsMember
from scouts_auth.groupadmin.serializers import AbstractScoutsMemberSerializer
from scouts_auth.groupadmin.services import GroupAdmin, ScoutsAuthorizationService


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsOIDCAuthenticationBackend(InuitsOIDCAuthenticationBackend):
    service = GroupAdmin()
    authorization_service = ScoutsAuthorizationService()

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
        member: AbstractScoutsMember = self.load_member_data(data=claims)
        user: settings.AUTH_USER_MODEL = self.UserModel.objects.create_user(
            username=username if username else member.username, email=member.email
        )
        user = self.merge_member_data(user, member, claims)

        logger.debug(
            "SCOUTS OIDC AUTHENTICATION: Created a user with username %s from member %s",
            user.username,
            member.group_admin_id,
        )

        return user

    def update_user(
        self, user: settings.AUTH_USER_MODEL, claims: dict
    ) -> settings.AUTH_USER_MODEL:
        """
        Update existing user with new claims if necessary, save, and return the updated user object.
        """
        member: AbstractScoutsMember = self.load_member_data(data=claims)
        user: settings.AUTH_USER_MODEL = self.merge_member_data(user, member, claims)

        logger.debug(
            "SCOUTS OIDC AUTHENTICATION: Updated a user with username %s ",
            user.username,
        )

        return user

    def load_member_data(self, data: dict) -> AbstractScoutsMember:
        serializer = AbstractScoutsMemberSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        member: AbstractScoutsMember = serializer.save()

        return member

    def merge_member_data(
        self, user: settings.AUTH_USER_MODEL, member: AbstractScoutsMember, claims: dict
    ) -> settings.AUTH_USER_MODEL:
        user.group_admin_id = member.group_admin_id
        user.gender = member.personal_data.gender
        user.phone_number = member.personal_data.phone_number
        user.membership_number = member.scouts_data.membership_number
        user.customer_number = member.scouts_data.customer_number
        user.birth_date = member.group_admin_data.birth_date
        user.first_name = member.group_admin_data.first_name
        user.last_name = member.group_admin_data.last_name
        user.email = member.email

        user.scouts_groups = member.scouts_groups
        user.addresses = member.addresses
        user.functions = member.functions
        user.group_specific_fields = member.group_specific_fields
        user.links = member.links

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
