from typing import List

from scouts_auth.auth.exceptions import ScoutsAuthException

from scouts_auth.groupadmin.models import AbstractScoutsGroup
from scouts_auth.groupadmin.models.fields import GroupAdminIdField
from scouts_auth.groupadmin.settings import GroupAdminSettings

from scouts_auth.inuits.models import AbstractNonModel, Gender
from scouts_auth.inuits.models.fields import OptionalCharField, ListField, OptionalEmailField


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsGroup():

    group_admin_id = GroupAdminIdField()
    number = OptionalCharField()
    name = OptionalCharField()
    email = OptionalEmailField()
    website = OptionalCharField()
    parent_group = GroupAdminIdField()
    child_groups = []
    type = OptionalCharField()

    def __init__(
        self,
        group_admin_id: str = None,
        number: str = None,
        name: str = None,
        email: str = None,
        website: str = None,
        parent_group: str = None,
        type: str = None
    ):
        self.group_admin_id = group_admin_id
        self.number = number
        self.name = name
        self.email = email
        self.website = website
        self.parent_group = parent_group
        self.type = type

    @property
    def gender(self) -> Gender:
        identifier = self.number.upper().strip()[-1]
        if identifier == GroupAdminSettings().get_group_gender_identifier_male():
            return Gender.MALE
        if identifier == GroupAdminSettings.get_group_gender_identifier_female():
            return Gender.FEMALE
        return Gender.MIXED

    @property
    def full_name(self):
        return "{} {}".format(self.name, self.group_admin_id)

    def add_child_group(self, child_group):
        if child_group not in self.child_groups:
            self.child_groups.append(child_group)

    def __str__(self):
        return (
            f"group_admin_id ({self.group_admin_id}), "
            f"number ({self.number}), "
            f"name ({self.name}), "
            f"email ({self.email}), "
            f"website ({self.website}), "
            f"parent_group ({self.parent_group}), "
            f"child_groups ({[str(child_group) for child_group in self.child_groups]}), "
            f"type ({self.type})"
        )

    @staticmethod
    def from_abstract_scouts_group(
        group=None,
        abstract_group: AbstractScoutsGroup = None
    ):
        if not abstract_group:
            raise ScoutsAuthException(
                "Can't construct a ScoutsGroup without an AbstractScoutsGroup")

        group = group if group else ScoutsGroup()

        group.group_admin_id = abstract_group.group_admin_id
        group.number = abstract_group.number
        group.name = abstract_group.name
        group.email = abstract_group.email
        group.website = abstract_group.website
        group.parent_group = abstract_group.parent_group
        group.type = abstract_group.type

        return group
