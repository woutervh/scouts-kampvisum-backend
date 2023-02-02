from types import SimpleNamespace

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.groups.models import ScoutsSection
from apps.groups.services import ScoutsSectionService

from scouts_auth.scouts.services import ScoutsPermissionService

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsUserHelperService:

    authorization_service = ScoutsPermissionService()
    section_service = ScoutsSectionService()

    handling_login = False
    handling_refresh = False
    handling_authentication = False

    def handle_oidc_login(
        self, user: settings.AUTH_USER_MODEL, **kwargs
    ) -> settings.AUTH_USER_MODEL:
        """
        Reads additional data for a user and takes appropriate action.

        Some user data necessary for permissions can only be loaded by a groupadmin profile call after authentication.
        This method handles a signal for the basic oidc authentication, then makes the necessary additional calls.
        """
        user: settings.AUTH_USER_MODEL = self._check_user_data(user=user)
        user: settings.AUTH_USER_MODEL = self._validate_user_data(user=user)
        user: settings.AUTH_USER_MODEL = self._cache_user_data(user=user)

        return user

    def handle_oidc_refresh(
        self, user: settings.AUTH_USER_MODEL, **kwargs
    ) -> settings.AUTH_USER_MODEL:
        user: settings.AUTH_USER_MODEL = self._check_user_data(user=user)
        user: settings.AUTH_USER_MODEL = self._validate_user_data(user=user)
        user: settings.AUTH_USER_MODEL = self._cache_user_data(user=user)

        return user

    def handle_oidc_authenticated(
        self, user: settings.AUTH_USER_MODEL, **kwargs
    ) -> settings.AUTH_USER_MODEL:
        """
        Reads additional data for a user and takes appropriate action.
        """
        return user

    def _check_user_data(
        self, user: settings.AUTH_USER_MODEL
    ) -> settings.AUTH_USER_MODEL:
        return user

    def _validate_user_data(
        self, user: settings.AUTH_USER_MODEL
    ) -> settings.AUTH_USER_MODEL:
        group_count: int = len(user.scouts_groups)
        persisted_group_count: int = len(user.scouts_groups)
        function_count: int = len(user.functions)
        persisted_function_count: int = user.persisted_scouts_functions.count()

        if group_count == 0 and persisted_group_count == 0:
            raise ValidationError(
                "No AbstractScoutsGroup instances loaded from groupadmin for user {}".format(
                    user.username
                )
            )
        if persisted_group_count == 0:
            raise ValidationError(
                "No ScoutsGroup instances were persisted for user {}".format(
                    user.username
                )
            )
        if function_count == 0 and persisted_function_count == 0:
            raise ValidationError(
                "No AbstractScoutsFunction instances loaded from groupadmin for user {}".format(
                    user.username
                )
            )
        if persisted_function_count == 0:
            raise ValidationError(
                "No ScoutsFunction instances were persisted for user {}".format(
                    user.username
                )
            )

        for group in user.scouts_groups:
            section_count: int = ScoutsSection.objects.all().filter(group=group)
            if section_count == 0:
                raise ValidationError(
                    "No ScoutsSection instances found for user {}".format(
                        user.username)
                )

        logger.debug(user.to_descriptive_string())

        return user

    def _cache_user_data(
        self, user: settings.AUTH_USER_MODEL
    ) -> settings.AUTH_USER_MODEL:
        # InuitsCache().store_user_data(user)

        # user = InuitsCache().retrieve_user_data(user.id)
        # logger.debug(
        #     "USER %s has %d groups and %d functions",
        #     user.username,
        #     len(user.scouts_groups),
        #     len(user.functions),
        # )
        # for group in user.scouts_groups:
        #     logger.debug("GROUP: %s", group.group_admin_id)
        #     logger.debug(
        #         "%s - SECTION LEADER: %s",
        #         group.group_admin_id,
        #         user.has_role_section_leader(group),
        #     )
        #     logger.debug(
        #         "%s - GROUP LEADER: %s",
        #         group.group_admin_id,
        #         user.has_role_group_leader(group),
        #     )
        # logger.debug(user.to_descriptive_string())

        return user
