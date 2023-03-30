import pytz
from typing import List
from datetime import datetime

from scouts_auth.auth.exceptions import ScoutsAuthException

from scouts_auth.groupadmin.models import (
    AbstractScoutsFunction,
    AbstractScoutsFunctionDescription,
    AbstractScoutsLink,
    AbstractScoutsFunctionCode,
    ScoutsGroup
)
from scouts_auth.groupadmin.models.fields import GroupAdminIdField

from scouts_auth.inuits.models import AbstractNonModel
from scouts_auth.inuits.models.fields import OptionalCharField, OptionalDateTimeField, OptionalDateField


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsFunction(AbstractNonModel):

    group_admin_id = GroupAdminIdField()
    begin = OptionalDateTimeField()
    end = OptionalDateTimeField()
    scouts_group = GroupAdminIdField()
    code = OptionalCharField()
    description = OptionalCharField()

    # Fields derived from the function description
    type = OptionalCharField()
    max_birth_date = OptionalDateField()
    adjunct = OptionalCharField()

    is_leader: bool = False

    class Meta:
        managed = False

    @property
    def scouts_function_code(self) -> AbstractScoutsFunctionCode:
        return AbstractScoutsFunctionCode(code=self.code)

    def is_active_function(self) -> bool:
        return not self.end or self.end <= pytz.utc.localize(datetime.now())

    def is_leader_function(self) -> bool:
        return self.is_leader

    def is_section_leader_function(self) -> bool:
        return self.is_leader_function()

    def is_group_leader_function(self) -> bool:
        return self.scouts_function_code.is_group_leader()

    def is_district_commissioner_function(self) -> bool:
        return self.scouts_function_code.is_district_commissioner()

    def is_shire_president_function(self) -> bool:
        return self.scouts_function_code.is_shire_president()

    def get_role_name(self) -> str:
        if self.is_shire_president_function():
            return "role_shire_president"
        if self.is_district_commissioner_function():
            return "role_district_commissioner"
        if self.is_group_leader_function():
            return "role_group_leader"
        if self.is_section_leader_function():
            return "role_section_leader"
        return "role_regular_member"

    def __str__(self):
        return (
            f"group_admin_id ({self.group_admin_id})"
            f"begin({self.begin})"
            f"end({self.end})"
            f"code ({self.code})"
            f"description ({self.description})"
            f"type ({self.type})"
            f"max_birth_date ({self.max_birth_date})"
            f"adjunct ({self.adjunct})"
            f"scouts_group ({self.scouts_group})"
        )

    def to_descriptive_string(self):
        return f"{self.code} - {self.description}: {self.scouts_group}"

    @staticmethod
    def from_abstract_function(
        scouts_function=None,
        abstract_function: AbstractScoutsFunction = None,
        abstract_function_description: AbstractScoutsFunctionDescription = None,
    ):
        if not abstract_function:
            raise ScoutsAuthException(
                "Can't construct a ScoutsFunction without an AbstractScoutsFunction")
        if not abstract_function_description:
            raise ScoutsAuthException(
                "Can't construct a ScoutsFunction without an AbstractScoutsFunctionDescription")

        scouts_function: ScoutsFunction = scouts_function if scouts_function else ScoutsFunction()

        scouts_function.group_admin_id = abstract_function.function
        scouts_function.begin = abstract_function.begin
        scouts_function.end = abstract_function.end
        scouts_function.code = abstract_function.code
        scouts_function.description = abstract_function.description
        scouts_function.type = abstract_function_description.type
        scouts_function.max_birth_date = abstract_function_description.max_birth_date
        scouts_function.adjunct = abstract_function_description.adjunct

        return scouts_function
