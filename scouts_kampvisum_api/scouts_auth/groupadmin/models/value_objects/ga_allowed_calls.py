from typing import List

from scouts_auth.groupadmin.models.value_objects import AbstractScoutsLink


class ScoutsAllowedCalls:
    links: List[AbstractScoutsLink]

    def __init__(self, links: List[AbstractScoutsLink] = None):
        self.links = links if links else []

    def __str__(self):
        return "links({})".format(", ".join(link for link in self.links))
