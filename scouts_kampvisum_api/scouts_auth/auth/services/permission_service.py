import yaml
import importlib
from typing import List

from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist

from scouts_auth.auth.exceptions import ScoutsAuthException
from scouts_auth.auth.settings import InuitsOIDCSettings
from scouts_auth.inuits.django import DjangoDbUtil


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class PermissionService:

    SUPER_ADMIN = "role_super_admin"

    _permission_groups = {}

    def add_user_to_group(
        self,
        user: settings.AUTH_USER_MODEL,
        group: Group = None,
        group_name: str = None,
    ) -> settings.AUTH_USER_MODEL:
        group: Group = self._get_group(group=group, group_name=group_name)

        logger.debug(
            f"Adding user to permission group {group.name}", user=user)

        group.user_set.add(user)

        user.is_superuser = (group.name == self.SUPER_ADMIN)

        user.full_clean()
        user.save()

        return user

    def remove_user_from_group(
        self,
        user: settings.AUTH_USER_MODEL,
        group: Group = None,
        group_name: str = None,
    ) -> settings.AUTH_USER_MODEL:
        group: Group = self._get_group(group=group, group_name=group_name)

        logger.debug(
            f"Removing user from permission group {group.name}", user=user)

        group.user_set.remove(user)

        user.full_clean()
        user.save()

        return user

    def _get_group(self, group: Group = None, group_name: str = None) -> Group:
        if not group and not group_name:
            raise ScoutsAuthException("Group or group name must be supplied")

        if group and group.name in self._permission_groups:
            return self._permission_groups.get(group.name)

        try:
            group: Group = Group.objects.get(name=group_name)

            self._permission_groups[group.name] = group

            return group
        except ObjectDoesNotExist:
            raise ScoutsAuthException(
                f"Permission group with name {group_name} does not exist")

    def setup_permission_groups(self):
        if not DjangoDbUtil.is_initial_db_ready():
            logger.debug(
                "Will not attempt to populate user permissions until migrations have been performed."
            )
            return

        try:
            self._populate_permission_groups()
        except Exception as exc:
            logger.error("Unable to populate user roles", exc)

    def _populate_permission_groups(self):
        # Will populate groups and add permissions to them, won't create permissions
        # these need to be created in models
        #
        # The roles.yaml file that links the permissions to the roles, is structured as this:
        # role_<name of role>:
        # - <app_label as defined in apps>.<name of permission>
        #
        # The permission names should be defined in the Meta class of a Model.
        # After a makemigrations and migrate, you can then specify the particular permissions that apply in the viewset
        import importlib.resources as pkg_resources

        roles_package = InuitsOIDCSettings.get_authorization_roles_config_package()
        roles_yaml = InuitsOIDCSettings.get_authorization_roles_config_yaml()

        # logger.debug(
        #     "SCOUTS_AUTH: importing roles and permissions from %s/%s",
        #     roles_package,
        #     roles_yaml,
        # )

        importlib.import_module(roles_package)
        yaml_data = pkg_resources.read_text(roles_package, roles_yaml)

        try:
            groups = yaml.safe_load(yaml_data)
            for group_name, permissions in groups.items():
                group: Group = Group.objects.get_or_create(name=group_name)[0]
                group_permissions = group.permissions.all()

                # Clean groups that no longer have permissions attached
                permissions = self._purge_group_permissions(
                    group_permissions, permissions
                )

                # Link permission groups to permission
                for permission in permissions:
                    self._add_permission_by_name(
                        group,
                        permission.get("codename"),
                        permission.get("app_label"),
                    )
                group.save()
        except yaml.YAMLError as exc:
            logger.error("Error while importing permissions groups", exc)

    def _purge_group_permissions(
        self, group_permissions: List[Permission], permissions: List[str]
    ) -> List[dict]:
        """
        Removes revoked and already existing permissions.

        Returns a list of dict with keys permission, codename and app_label.
        """
        # Avoid clearing the table and adding the same permission over and over again,
        # but avoid even more to keep a permission that was revoked.
        parsed_permissions: List[dict] = []
        for permission in permissions:
            permission_parts = permission.split(".")
            parsed_permissions.append(
                {
                    "permission": permission,
                    "codename": permission_parts[1],
                    "app_label": permission_parts[0],
                }
            )

        # Remove group permissions that have been revoked and keep only new permissions
        remove_permissions: List[str] = []
        for group_permission in group_permissions:
            remove_permission = True
            for parsed_permission in parsed_permissions:
                if (
                    parsed_permission.get(
                        "codename") == group_permission.codename
                    and parsed_permission.get("app_label")
                    == group_permission.content_type.app_label
                ):
                    # The group already has this permission, remove it from the list
                    remove_permissions.append(parsed_permission)
                    remove_permission = False
                    break

            # If we're here, then the group permission has been revoked
            if remove_permission:
                group_permission.delete()

        for remove_permission in remove_permissions:
            parsed_permissions.remove(remove_permission)

        # Return a list of permissions
        return parsed_permissions

    @staticmethod
    def _add_permission_by_name(
        group: Group, codename: str, app_label: str
    ):
        try:
            logger.debug(
                f"Retrieving permission with codename {codename} for app {app_label}")
            permission = Permission.objects.get(
                codename=codename, content_type__app_label=app_label
            )
            group.permissions.add(permission)
        except ObjectDoesNotExist:
            raise ScoutsAuthException(
                f"Permission {permission} with codename {codename} doesn't exist for app_label {app_label}"
            )
