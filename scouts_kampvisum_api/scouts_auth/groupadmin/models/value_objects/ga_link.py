from typing import List

from django.db import models

from scouts_auth.inuits.models import AbstractNonModel
from scouts_auth.inuits.models.fields import OptionalCharField


class AbstractScoutsLink(AbstractNonModel):
    """This class captures the data returned by GroupAdmin containing links to the full references info."""

    rel = OptionalCharField()
    href = OptionalCharField()
    method = OptionalCharField()
    sections: List[str] = models.JSONField()

    class Meta:
        abstract = True

    def __init__(self, rel: str = "", href: str = "", method: str = "", sections: List[str] = None):
        self.rel = rel
        self.href = href
        self.method = method
        self.sections = sections if sections else []

        # super().__init__([], {})

    def __str__(self):
        return "rel({}), href({}), method({}), sections({})".format(
            self.rel,
            self.href,
            self.method,
            ", ".join(str(section) for section in self.sections),
        )
