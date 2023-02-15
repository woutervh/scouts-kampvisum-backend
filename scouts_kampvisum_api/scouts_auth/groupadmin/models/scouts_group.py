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


class ScoutsGroup(AbstractNonModel):

    group_admin_id = GroupAdminIdField()
    number = OptionalCharField()
    name = OptionalCharField()
    email = OptionalEmailField()
    website = OptionalCharField()
    parent_group = GroupAdminIdField()
    _child_group_names = None
    type = OptionalCharField()

    class Meta:
        managed = False

    def __init__(
        self,
        group_admin_id: str = None,
        number: str = None,
        name: str = None,
        email: str = None,
        website: str = None,
        parent_group: str = None,
        type: str = None,
        _child_group_names: List[str] = None,
    ):
        self.group_admin_id = group_admin_id
        self.number = number
        self.name = name
        self.email = email
        self.website = website
        self.parent_group = parent_group
        self.type = type
        self._child_group_names = _child_group_names if _child_group_names else []

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

    def add_child_group(self, child_group: str):
        if not self._child_group_names:
            self._child_group_names = []
        if child_group not in self._child_group_names:
            self._child_group_names.append(child_group)

    def has_child_groups(self) -> bool:
        return self._child_group_names and isinstance(self._child_group_names, list) and len(self._child_group_names) > 0

    def get_child_groups(self) -> List[str]:
        return self._child_group_names

    def is_admin_group(self) -> bool:
        return self.group_admin_id in GroupAdminSettings.get_administrator_groups()

    def __str__(self):
        return (
            f"group_admin_id ({self.group_admin_id}), "
            f"number ({self.number}), "
            f"name ({self.name}), "
            f"email ({self.email}), "
            f"website ({self.website}), "
            f"parent_group ({self.parent_group}), "
            f"child_groups ({[str(child_group) for child_group in self._child_group_names]}), "
            f"type ({self.type})"
        )

    def __key__(self):
        return (self.group_admin_id, )

    def __hash__(self):
        return hash(self.__key__())

    def __eq__(self, other):
        if isinstance(other, ScoutsGroup):
            return self.__hash__() == other.__hash__()
        return NotImplemented

    @staticmethod
    def from_abstract_scouts_group(
        scouts_group=None,
        abstract_group: AbstractScoutsGroup = None
    ):
        if not abstract_group:
            raise ScoutsAuthException(
                "Can't construct a ScoutsGroup without an AbstractScoutsGroup")

        scouts_group = scouts_group if scouts_group else ScoutsGroup()

        scouts_group.group_admin_id = abstract_group.group_admin_id
        scouts_group.number = abstract_group.number
        scouts_group.name = abstract_group.name
        scouts_group.email = abstract_group.email
        scouts_group.website = abstract_group.website
        scouts_group.parent_group = abstract_group.parent_group
        scouts_group.type = abstract_group.type

        return scouts_group
