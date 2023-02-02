from typing import List
from datetime import date, datetime


from scouts_auth.groupadmin.models.fields import OptionalGroupAdminIdField
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
)


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class AbstractScoutsFunctionDescription(AbstractNonModel):

    group_admin_id = OptionalGroupAdminIdField()
    type = OptionalCharField()
    max_birth_date = OptionalDateField()
    code = OptionalCharField()
    description = OptionalCharField()
    adjunct = OptionalCharField()

    # Declare as foreign keys in concrete subclasses
    scouts_groups: List[AbstractScoutsGroup] = []
    groupings: List[AbstractScoutsGrouping] = []
    links: List[AbstractScoutsLink] = []

    # Runtime data
    _scouts_function_code: AbstractScoutsFunctionCode = None

    class Meta:
        abstract = True

    def __init__(
        self,
        group_admin_id: str = None,
        type: str = None,
        scouts_groups: List[AbstractScoutsGroup] = None,
        groupings: List[AbstractScoutsGrouping] = None,
        begin: datetime = None,
        end: datetime = None,
        max_birth_date: date = None,
        code: str = None,
        description: str = None,
        adjunct: str = None,
        links: List[AbstractScoutsLink] = None,
    ):
        self.group_admin_id = group_admin_id
        self.type = type
        self.scouts_groups = scouts_groups
        self.groupings = groupings
        self.begin = begin
        self.end = end
        self.max_birth_date = max_birth_date
        self.code = code
        self.description = description
        self.adjunct = adjunct
        self.links = links if links else []

    # Necessary for comparison
    @property
    def pk(self):
        return self.group_admin_id

    @property
    def function_code(self):
        if self._scouts_function_code is None:
            self._scouts_function_code = AbstractScoutsFunctionCode(self.code)
        return self._scouts_function_code

    def get_groupings_name(self):
        index = 0
        name = None
        for grouping in self.groupings:
            if grouping.index > index:
                index = grouping.index
                name = grouping.name

        return name

    def __str__(self):
        return "group_admin_id ({}), type ({}), scouts_groups({}), groupings({}), begin({}), end ({}), max_birth_date ({}), code({}), description({}), adjunct ({}), links({})".format(
            self.group_admin_id,
            self.type,
            ", ".join(str(group) for group in self.scouts_groups)
            if self.scouts_groups
            else "[]",
            ", ".join(str(grouping) for grouping in self.groupings)
            if self.groupings
            else "[]",
            self.begin,
            self.end,
            self.max_birth_date,
            self.code,
            self.description,
            self.adjunct,
            ", ".join(str(link)
                      for link in self.links) if self.links else "[]",
        )

    def to_descriptive_string(self):
        return "{} -> {} ({}),".format(self.group_admin_id, self.code, self.description)
