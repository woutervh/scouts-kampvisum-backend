from typing import List

from scouts_auth.groupadmin.models.value_objects import AbstractScoutsLink
from scouts_auth.inuits.models import AbstractNonModel


class AbstractScoutsResponse(AbstractNonModel):
    """
    Class to capture composite responses, that typically contain a list of links and a list of objects.
    """

    count: int
    total: int
    offset: int
    filter_criterium: str
    criteria: dict
    links: List[AbstractScoutsLink]

    class Meta:
        abstract = True

    def __init__(
        self,
        count: int = 0,
        total: int = 0,
        offset: int = 0,
        filter_criterium: str = "",
        criteria: dict = None,
        links: List[AbstractScoutsLink] = None,
    ):
        self.count = count
        self.total = total
        self.offset = offset
        self.filter_criterium = filter_criterium
        self.criteria = criteria if criteria else {}
        self.links = links if links else []

        # super().__init__([], {})

    def __str__(self):
        return "count({}), total({}), offset({}), filter_criterium({}), criteria({}), links: ({})".format(
            self.count,
            self.total,
            self.offset,
            self.filter_criterium,
            ", ".join((str(key) + "(" + str(self.criteria[key]) + ")") for key in self.criteria.keys()),
            ", ".join(str(link) for link in self.links),
        )
