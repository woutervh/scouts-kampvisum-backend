from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.exceptions import ValidationError
from django.dispatch import receiver

from apps.groups.models import ScoutsSection
from apps.groups.services import ScoutsSectionService

from scouts_auth.auth.signals import (
    ScoutsAuthSignalSender,
    app_ready,
    oidc_login,
    oidc_refresh,
    oidc_authenticated,
)
from scouts_auth.auth.services import PermissionService
from scouts_auth.auth.oidc_user_helper import OIDCUserHelper

from scouts_auth.groupadmin.services import ScoutsAuthorizationService

from scouts_auth.inuits.cache import InuitsCache

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class SignalHandlerService:

    handling_login = False
    handling_refresh = False
    handling_authentication = False

    @staticmethod
    @receiver(
        app_ready,
        sender=ScoutsAuthSignalSender.sender,
        dispatch_uid=ScoutsAuthSignalSender.app_ready_uid,
    )
    def handle_app_ready(**kwargs):
        signal = "app_ready"
        logger.debug(
            "SIGNAL received: '%s' from %s", signal, ScoutsAuthSignalSender.sender
        )
        if not SignalHandlerService._is_initial_db_ready():
            logger.debug(
                "Will not attempt to populate user permissions until migrations have been performed."
            )
            return

        try:
            logger.debug("Populating user permissions")
            PermissionService().populate_roles()
        except Exception as exc:
            logger.error("Unable to populate user roles", exc)

    @staticmethod
    @receiver(
        oidc_login,
        sender=ScoutsAuthSignalSender.sender,
        dispatch_uid=ScoutsAuthSignalSender.authenticated_uid,
    )
    def handle_oidc_login(
        user: settings.AUTH_USER_MODEL, **kwargs
    ) -> settings.AUTH_USER_MODEL:
        """
        Reads additional data for a user and takes appropriate action.

        Some user data necessary for permissions can only be loaded by a groupadmin profile call after authentication.
        This method handles a signal for the basic oidc authentication, then makes the necessary additional calls.
        """
        if SignalHandlerService.handling_login:
            return
        SignalHandlerService.handling_login = True
        signal = "oidc_login"

        logger.debug(
            "SIGNAL received: '%s' from %s", signal, ScoutsAuthSignalSender.sender
        )
        logger.debug("LOGGED IN USER: %s (%s)", user.username, type(user).__name__)

        user: settings.AUTH_USER_MODEL = SignalHandlerService._check_user_data(
            user=user, signal=signal
        )

        SignalHandlerService.handling_login = False

        return user

    @staticmethod
    @receiver(
        oidc_refresh,
        sender=ScoutsAuthSignalSender.sender,
        dispatch_uid=ScoutsAuthSignalSender.refreshed_uid,
    )
    def handle_oidc_refresh(
        user: settings.AUTH_USER_MODEL, **kwargs
    ) -> settings.AUTH_USER_MODEL:
        if SignalHandlerService.handling_refresh:
            return
        SignalHandlerService.handling_refresh = True
        signal = "oidc_refresh"

        logger.debug(
            "SIGNAL received: '%s' from %s", signal, ScoutsAuthSignalSender.sender
        )
        logger.debug("REFRESHED USER: %s (%s)", user.username, type(user).__name__)

        user: settings.AUTH_USER_MODEL = SignalHandlerService._check_user_data(
            user=user, signal=signal
        )

        SignalHandlerService.handling_refresh = False

        return user

    @staticmethod
    @receiver(
        oidc_authenticated,
        sender=ScoutsAuthSignalSender.sender,
        dispatch_uid=ScoutsAuthSignalSender.authenticated_uid,
    )
    def handle_oidc_authenticated(
        user: settings.AUTH_USER_MODEL, **kwargs
    ) -> settings.AUTH_USER_MODEL:
        """
        Reads additional data for a user and takes appropriate action.

        Some user data necessary for permissions can only be loaded by a groupadmin profile call after authentication.
        This method handles a signal for the basic oidc authentication, then makes the necessary additional calls.
        """
        if SignalHandlerService.handling_authentication:
            return
        SignalHandlerService.handling_authentication = True
        signal = "oidc_authenticated"

        logger.debug(
            "SIGNAL received: '%s' from %s", signal, ScoutsAuthSignalSender.sender
        )
        logger.debug("AUTHENTICATED USER: %s (%s)", user.username, type(user).__name__)

        SignalHandlerService.handling_authentication = False

        return user

    @staticmethod
    def _is_initial_db_ready() -> bool:
        try:
            content_types = ContentType.objects.all()

            if content_types:
                return True
        except:
            logger.debug(
                "Unable to load authentication groups, database is probably not ready yet"
            )

        return False

    @staticmethod
    def _check_user_data(
        user: settings.AUTH_USER_MODEL, signal: str
    ) -> settings.AUTH_USER_MODEL:
        authorization_service = ScoutsAuthorizationService()
        section_service = ScoutsSectionService()

        if not OIDCUserHelper.requires_data_loading(user=user):
            return user

        # if OIDCUserHelper.requires_group_loading(user=user):
        #     logger.debug(
        #         "SIGNAL handling for '%s' -> Loading additional user groups", signal
        #     )
        #     user = authorization_service.load_user_scouts_groups(user=user)
        try:
            logger.debug(
                "SIGNAL handling for '%s' -> Loading additional user groups", signal
            )
            user = authorization_service.load_user_scouts_groups(user=user)
        except Exception as exc:
            raise ValidationError(
                "An error occured while loading user scouts groups", exc
            )
        # if OIDCUserHelper.requires_function_loading(user=user):
        #     logger.debug("SIGNAL handling for '%s' -> Loading scouts functions", signal)
        #     user = authorization_service.load_user_functions(user=user)
        try:
            logger.debug("SIGNAL handling for '%s' -> Loading scouts functions", signal)
            user = authorization_service.load_user_functions(user=user)
        except Exception as exc:
            raise ValidationError(
                "An error occured while loading user scouts functions", exc
            )

        try:
            logger.debug(
                "SIGNAL handling for '%s' -> Setting up sections for user's groups",
                signal,
            )
            section_service.setup_default_sections(user=user)
        except Exception as exc:
            raise ValidationError(
                "An error occured while setting up default scouts sections", exc
            )

        user: settings.AUTH_USER_MODEL = SignalHandlerService._cache_user_data(
            user=user, signal=signal
        )

        group_count: int = len(user.scouts_groups)
        persisted_group_count: int = user.persisted_scouts_groups.count()
        function_count: int = len(user.functions)
        persisted_function_count: int = user.persisted_scouts_functions.count()
        section_count: int = ScoutsSection.objects.all().filter(
            group__in=user.persisted_scouts_groups.all()
        )

        if group_count == 0:
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
        if function_count == 0:
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
        if section_count == 0:
            raise ValidationError(
                "No ScoutsSection instances found for user {}".format(user.username)
            )

        logger.debug(user.to_descriptive_string())

        return user

    @staticmethod
    def _cache_user_data(
        user: settings.AUTH_USER_MODEL, signal: str
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
