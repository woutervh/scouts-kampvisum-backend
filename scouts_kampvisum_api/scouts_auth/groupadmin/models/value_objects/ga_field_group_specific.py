from typing import List

from django.db import models

from scouts_auth.groupadmin.models.value_objects import AbstractScoutsValue

from scouts_auth.inuits.models import AbstractNonModel
from scouts_auth.inuits.models.fields import OptionalCharField


class AbstractScoutsGroupSpecificField(AbstractNonModel):

    group_admin_id = OptionalCharField()
    schema = models.JSONField()
    values: List[AbstractScoutsValue]

    class Meta:
        abstract = True

    def __init__(
        self,
        group: str = None,
        schema: List[str] = None,
        values: List[AbstractScoutsValue] = None,
    ):
        self.group = group
        self.schema = schema if schema else []
        self.values = values if values else []

        # super().__init__([], {})

    def __str__(self):
        return "group ({}), schema({}), values({})".format(
            self.group,
            ", ".join(schema_item for schema_item in self.schema)
            if self.schema
            else "[]",
            ", ".join(value for value in self.values) if self.values else "[]",
        )
