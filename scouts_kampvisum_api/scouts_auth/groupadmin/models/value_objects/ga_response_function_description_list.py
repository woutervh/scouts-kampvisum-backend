from typing import List, Tuple

from scouts_auth.groupadmin.models.value_objects import (
    AbstractScoutsFunctionDescription,
    AbstractScoutsLink,
)
from scouts_auth.inuits.models import AbstractNonModel


class AbstractScoutsFunctionDescriptionListResponse(AbstractNonModel):

    function_descriptions: List[AbstractScoutsFunctionDescription]
    links: List[AbstractScoutsLink]

    class Meta:
        abstract = True

    def __init__(
        self,
        function_descriptions: List[AbstractScoutsFunctionDescription] = None,
        links: List[AbstractScoutsLink] = None,
    ):
        self.function_descriptions = (
            function_descriptions if function_descriptions else []
        )
        self.links = links if links else []

        # super().__init__([], {})

    def get_function_codes(self) -> List[str]:
        return [
            function_description.code
            for function_description in self.function_descriptions
        ]

    def get_descriptive_function_codes(self) -> List[Tuple]:
        return [
            (function_description.code, function_description.description)
            for function_description in self.function_descriptions
        ]

    def get_printable_descriptive_function_codes(self) -> str:
        return "\n".join(
            function_description.code + "," + function_description.description
            for function_description in self.function_descriptions
        )

    def __str__(self):
        return "functions({}), links({})".format(
            ", ".join(
                str(function_description)
                for function_description in self.function_descriptions
            ),
            ", ".join(str(link) for link in self.links) if self.links else "[]",
        )
