import logging

from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist


logger = logging.getLogger(__name__)


class AuthorizationService:

    SUPER_ADMIN = "role_super_admin"

    def add_user_to_group(self, user: User, group: Group = None, group_name: str = None) -> User:
        if not group and not group_name:
            raise ValueError("Group or group name must be supplied")

        if not group:
            try:
                group: Group = Group.objects.get(name=group_name)
            except ObjectDoesNotExist:
                logger.error("Auth group with name %s does not exist", group_name)
                raise Exception

        logger.debug("Adding user %s to auth group %s", user.username, group.name)
        group.user_set.add(user)

        if group.name == self.SUPER_ADMIN:
            user.is_superuser = True

        return user
