from typing import List
from datetime import datetime

from scouts_auth.groupadmin.models.value_objects import (
    AbstractScoutsGroup,
    AbstractScoutsLink,
)
from scouts_auth.groupadmin.models.fields import OptionalGroupAdminIdField
from scouts_auth.groupadmin.models.enums import AbstractScoutsFunctionCode

from scouts_auth.inuits.models import AbstractNonModel
from scouts_auth.inuits.models.fields import (
    OptionalCharField,
    OptionalDateTimeField,
)


class AbstractScoutsFunction(AbstractNonModel):

    function = OptionalGroupAdminIdField()
    begin = OptionalDateTimeField()
    end = OptionalDateTimeField()

    code = OptionalCharField()
    description = OptionalCharField()

    # Declare as foreign keys in concrete subclasses
    scouts_group: AbstractScoutsGroup = None

    links: List[AbstractScoutsLink]

    # Runtime data
    _scouts_function_code: AbstractScoutsFunctionCode = None

    class Meta:
        abstract = True

    def __init__(
        self,
        scouts_group: AbstractScoutsGroup = None,
        function: str = None,
        begin: datetime = None,
        end: datetime = None,
        code: str = None,
        description: str = None,
        links: List[AbstractScoutsLink] = None,
    ):
        self.function = function
        self.scouts_group = scouts_group
        self.begin = begin
        self.end = end
        self.code = code
        self.description = description
        self.links = links if links else []

    # Necessary for comparison
    @property
    def pk(self):
        return self.function

    @property
    def function_code(self):
        if self._scouts_function_code is None:
            self._scouts_function_code = AbstractScoutsFunctionCode(self.code)
        return self._scouts_function_code

    def __str__(self):
        return "function({}), scouts_group({}), begin({}), end ({}), code({}), description({}), links({})".format(
            self.function,
            str(self.scouts_group),
            self.begin,
            self.end,
            self.code,
            self.description,
            ", ".join(str(link)
                      for link in self.links) if self.links else "[]",
        )

    def to_descriptive_string(self):
        return "{} -> {} ({}),".format(
            self.scouts_group.group_admin_id, self.code, self.description
        )
