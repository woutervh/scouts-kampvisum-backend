import yaml, importlib
from typing import List

from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist

from scouts_auth.auth.settings import OIDCSettings


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class PermissionService:
    def populate_roles(self, **kwargs):
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

        roles_package = OIDCSettings.get_authorization_roles_config_package()
        roles_yaml = OIDCSettings.get_authorization_roles_config_yaml()

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
                # @TODO clean groups that no longer have permissions attached
                group: Group = Group.objects.get_or_create(name=group_name)[0]
                group_permissions = group.permissions.all()

                permissions = self._purge_group_permissions(
                    group, group_permissions, permissions
                )

                # logger.debug(
                #     "Adding %d PERMISSIONS to group %s", len(permissions), group_name
                # )
                for permission in permissions:
                    self._add_permission_by_name(
                        group,
                        permission.get("permission"),
                        permission.get("codename"),
                        permission.get("app_label"),
                    )
                group.save()
        except yaml.YAMLError as exc:
            logger.error("Error while importing permissions groups", exc)

    def _purge_group_permissions(
        self, group: Group, group_permissions: List[Permission], permissions: List[str]
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
                    parsed_permission.get("codename") == group_permission.codename
                    and parsed_permission.get("app_label")
                    == group_permission.content_type.app_label
                ):
                    # The group already has this permission, remove it from the list
                    remove_permissions.append(parsed_permission)
                    remove_permission = False
                    break

            # If we're here, then the group permission has been revoked
            if remove_permission:
                # logger.debug(
                #     "Removing permission %s.%s from group %s",
                #     group_permission.content_type.app_label,
                #     group_permission.codename,
                #     group.name,
                # )
                group_permission.delete()

        for remove_permission in remove_permissions:
            parsed_permissions.remove(remove_permission)

        # Return a list of permissions
        return parsed_permissions

    def _add_permission_by_name(
        self, group: Group, permission: str, codename: str, app_label: str
    ):
        try:
            permission = Permission.objects.get(
                codename=codename, content_type__app_label=app_label
            )
            group.permissions.add(permission)
        except ObjectDoesNotExist:
            logger.error(
                "Permission %s with codename %s doesn't exist for app_label %s",
                permission,
                codename,
                app_label,
            )
