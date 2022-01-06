import logging
from django.db import models

from apps.camps.models import CampYear
from apps.groups.models import ScoutsSection

from scouts_auth.inuits.models import AuditedBaseModel
from scouts_auth.inuits.models.fields import OptionalDateField


logger = logging.getLogger(__name__)


class Camp(AuditedBaseModel):
    """
    A model for a scouts camp.
    """

    # @TODO model period, exceptions, test-driven
    year = models.ForeignKey(CampYear, on_delete=models.CASCADE)
    name = models.TextField()
    start_date = OptionalDateField()
    end_date = OptionalDateField()
    sections = models.ManyToManyField(ScoutsSection)

    class Meta:
        ordering = ["start_date"]

    def get_group_type(self):
        """
        Convenience method for getting the group type from the sections
        """
        for section in self.sections.all():
            return section.group.type

    def __str__(self):
        return "OBJECT Camp: year({}), name({}), start_date({}), end_date({}), sections({})".format(
            str(self.year),
            self.name,
            self.start_date,
            self.end_date,
            str(self.sections),
        )

    def to_simple_str(self):
        return "Camp ({}), {} {}".format(self.id, self.year.year, self.name)
