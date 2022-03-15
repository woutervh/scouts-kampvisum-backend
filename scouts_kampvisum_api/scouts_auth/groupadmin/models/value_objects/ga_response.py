from typing import List

from scouts_auth.groupadmin.models.value_objects import AbstractScoutsLink
from scouts_auth.inuits.models import AbstractNonModel


class AbstractScoutsResponse(AbstractNonModel):
    """
    Class to capture composite responses, that typically contain a list of links and a list of objects.
    """

    count: int = 0
    total: int = 0
    offset: int = 0
    filter_criterium: str = ""
    criteria: dict = {}
    links: List[AbstractScoutsLink] = []

    class Meta:
        abstract = True

    def __init__(
        self,
        count: int = None,
        total: int = None,
        offset: int = None,
        filter_criterium: str = None,
        criteria: dict = {},
        links: List[AbstractScoutsLink] = [],
    ):
        self.count = count if count else 0
        self.total = total if total else 0
        self.offset = offset if offset else 0
        self.filter_criterium = filter_criterium if filter_criterium else ""
        self.criteria = criteria if criteria else {}
        self.links = links if links else []

        # super().__init__([], {})

    def __str__(self):
        return "count({}), total({}), offset({}), filter_criterium({}), criteria({}), links: ({})".format(
            self.count,
            self.total,
            self.offset,
            self.filter_criterium,
            ", ".join(
                (str(key) + "(" + str(self.criteria[key]) + ")")
                for key in self.criteria.keys()
            ),
            ", ".join(str(link) for link in self.links) if self.links else "[]",
        )
