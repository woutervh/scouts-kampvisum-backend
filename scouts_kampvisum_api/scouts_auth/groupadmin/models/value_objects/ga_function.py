from typing import List, Dict
from datetime import date, datetime

from scouts_auth.groupadmin.models.value_objects import AbstractScoutsGroup, AbstractScoutsGrouping, AbstractScoutsLink
from scouts_auth.groupadmin.models.enums import AbstractScoutsFunctionCode


class AbstractScoutsFunction:

    group_admin_id: str
    type: str
    scouts_group: AbstractScoutsGroup
    function: str
    scouts_groups: List[AbstractScoutsGroup]
    groupings: List[AbstractScoutsGrouping]
    begin: datetime
    end: datetime
    max_birth_date: date
    code: str
    description: str
    adjunct: str
    links: List[AbstractScoutsLink]

    _scouts_function_code: AbstractScoutsFunctionCode = None
    groups_section_leader: Dict[str, bool]
    groups_group_leader: Dict[str, bool]
    is_district_commissioner: bool = False

    def __init__(
        self,
        group_admin_id: str = "",
        type: str = "",
        scouts_group: AbstractScoutsGroup = None,
        function: str = "",
        scouts_groups: List[AbstractScoutsGroup] = None,
        groupings: List[AbstractScoutsGrouping] = None,
        begin: datetime = None,
        end: datetime = None,
        max_birth_date: date = None,
        code: str = "",
        description: str = "",
        adjunct: str = "",
        links: List[AbstractScoutsLink] = None,
        groups_section_leader: Dict[str, bool] = None,
        groups_group_leader: Dict[str, bool] = None,
    ):
        self.group_admin_id = group_admin_id
        self.type = type
        self.function = function
        self.scouts_group = scouts_group
        self.scouts_groups = scouts_groups
        self.groupings = groupings
        self.begin = begin
        self.end = end
        self.max_birth_date = max_birth_date
        self.code = code
        self.description = description
        self.adjunct = adjunct
        self.links = links if links else []
        self.groups_section_leader = groups_section_leader if groups_section_leader else {}
        self.groups_group_leader = groups_group_leader if groups_group_leader else {}

    def _parse_function_code(self):
        if self._scouts_function_code is None:
            self._scouts_function_code = AbstractScoutsFunctionCode(self.code)
        return self._scouts_function_code

    def is_section_leader(self, group: AbstractScoutsGroup) -> bool:
        return self.groups_section_leader.get(group.group_admin_id, False)

    def is_group_leader(self, group: AbstractScoutsGroup) -> bool:
        return (
            self._parse_function_code().is_group_leader() and self.scouts_group.group_admin_id == group.group_admin_id
        )

    def is_district_commissioner(self) -> bool:
        return self._parse_function_code().is_district_commissioner()

    def __str__(self):
        return "group_admin_id ({}), type ({}), function({}), scouts_group({}), scouts_groups({}), groupings({}), begin({}), end ({}), max_birth_date ({}), code({}), description({}), adjunct ({}), links({})".format(
            self.group_admin_id,
            self.type,
            self.function,
            str(self.scouts_group),
            ", ".join(str(group) for group in self.scouts_groups),
            ", ".join(str(grouping) for grouping in self.groupings),
            self.begin,
            self.end,
            self.max_birth_date,
            self.code,
            self.description,
            self.adjunct,
            ", ".join(str(link) for link in self.links),
        )

    def to_descriptive_string(self):
        return "{} -> {} ({})".format(self.scouts_group.group_admin_id, self.code, self.description)
