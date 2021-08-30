import logging
from django.db import models

from ..models import CampYear
from apps.base.models import BaseModel
from apps.groups.api.models import Section
from inuits.mixins import CreatedByMixin, AuditTimestampMixin
from inuits.models import OptionalDateField


logger = logging.getLogger(__name__)


class Camp(CreatedByMixin, AuditTimestampMixin, BaseModel):
    """
    A model for a scouts camp.
    """

    # @TODO model period, exceptions, test-driven
    year = models.ForeignKey(CampYear, on_delete=models.CASCADE)
    name = models.TextField()
    start_date = OptionalDateField()
    end_date = OptionalDateField()
    sections = models.ManyToManyField(Section)

    class Meta:
        ordering = ["start_date"]

    def get_group_type(self):
        """
        Convenience method for getting the group type from the sections
        """
        for section in self.sections.all():
            return section.group.type
