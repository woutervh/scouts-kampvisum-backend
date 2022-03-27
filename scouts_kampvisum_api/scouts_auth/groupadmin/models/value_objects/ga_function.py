from typing import List, Dict
from datetime import date, datetime

from scouts_auth.groupadmin.models.value_objects import (
    AbstractScoutsGroup,
    AbstractScoutsGrouping,
    AbstractScoutsLink,
)
from scouts_auth.groupadmin.models.enums import AbstractScoutsFunctionCode
from scouts_auth.inuits.models import AbstractNonModel
from scouts_auth.inuits.models.fields import (
    OptionalCharField,
    OptionalDateField,
    OptionalDateTimeField,
)


class AbstractScoutsFunction(AbstractNonModel):

    group_admin_id = OptionalCharField()
    function = OptionalCharField()
    begin = OptionalDateTimeField()
    end = OptionalDateTimeField()

    code = OptionalCharField()
    description = OptionalCharField()

    # Declare as foreign keys in concrete subclasses
    scouts_group: AbstractScoutsGroup

    links: List[AbstractScoutsLink]

    # Runtime data
    _scouts_function_code: AbstractScoutsFunctionCode = None
    groups_section_leader: Dict[str, bool]
    groups_group_leader: Dict[str, bool]
    is_district_commissioner: bool = False

    class Meta:
        abstract = True

    def __init__(
        self,
        group_admin_id: str = None,
        scouts_group: AbstractScoutsGroup = None,
        function: str = None,
        begin: datetime = None,
        end: datetime = None,
        code: str = None,
        description: str = None,
        links: List[AbstractScoutsLink] = None,
        groups_section_leader: Dict[str, bool] = None,
        groups_group_leader: Dict[str, bool] = None,
    ):
        self.group_admin_id = group_admin_id
        self.function = function
        self.scouts_group = scouts_group
        self.begin = begin
        self.end = end
        self.code = code
        self.description = description
        self.links = links if links else []

    @property
    def function_code(self):
        if self._scouts_function_code is None:
            self._scouts_function_code = AbstractScoutsFunctionCode(self.code)
        return self._scouts_function_code

    def is_section_leader(self, group: AbstractScoutsGroup) -> bool:
        return self.groups_section_leader.get(group.group_admin_id, False)

    def is_group_leader(self, group: AbstractScoutsGroup) -> bool:
        return (
            self.function_code.is_group_leader()
            and self.scouts_group.group_admin_id == group.group_admin_id
        )

    def is_district_commissioner(self) -> bool:
        return self.function_code.is_district_commissioner()

    def __str__(self):
        return "group_admin_id ({}), function({}), scouts_group({}), begin({}), end ({}), code({}), description({}), links({})".format(
            self.group_admin_id,
            self.function,
            str(self.scouts_group),
            self.begin,
            self.end,
            self.code,
            self.description,
            ", ".join(str(link) for link in self.links) if self.links else "[]",
        )

    def to_descriptive_string(self):
        return "{} -> {} ({}),".format(
            self.scouts_group.group_admin_id, self.code, self.description
        )
