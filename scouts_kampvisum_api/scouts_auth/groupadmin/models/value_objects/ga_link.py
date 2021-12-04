from typing import List


class AbstractScoutsLink:
    """This class captures the data returned by GroupAdmin containing links to the full references info."""

    rel: str
    href: str
    method: str
    sections: List[str]

    def __init__(self, rel: str = "", href: str = "", method: str = "", sections: List[str] = None):
        self.rel = rel
        self.href = href
        self.method = method
        self.sections = sections if sections else []

    def __str__(self):
        return "rel({}), href({}), method({}), sections({})".format(
            self.rel,
            self.href,
            self.method,
            ", ".join(str(section) for section in self.sections),
        )
