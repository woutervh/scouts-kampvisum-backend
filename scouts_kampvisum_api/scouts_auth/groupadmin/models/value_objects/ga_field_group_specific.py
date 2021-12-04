from typing import List

from scouts_auth.groupadmin.models.value_objects import AbstractScoutsValue


class AbstractScoutsGroupSpecificField:

    group_admin_id: str
    schema: List[str]
    values: List[AbstractScoutsValue]

    def __init__(self, group: str = None, schema: List[str] = None, values: List[AbstractScoutsValue] = None):
        self.group = group
        self.schema = schema if schema else []
        self.values = values if values else []

    def __str__(self):
        return "group ({}), schema({}), values({})".format(
            self.group,
            ", ".join(schema_item for schema_item in self.schema),
            ", ".join(value for value in self.values),
        )
