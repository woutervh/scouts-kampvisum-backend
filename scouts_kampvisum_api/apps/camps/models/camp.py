import logging
from django.db import models
from django.core.exceptions import ValidationError

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

    def clean(self):
        if not self.name:
            raise ValidationError("A Camp must have a name")
        # This can't be done, because there is no Camp instance yet.
        # Validate the presence of at least 1 Section in uuid in the
        # serializer's validate method.
        # if not self.sections or len(self.sections) == 0:
        #    raise ValidationError(
        #        "A Camp must have at least 1 Section attached")
