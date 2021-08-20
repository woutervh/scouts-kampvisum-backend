import logging
from django.db import models
from django.core.exceptions import ValidationError

from apps.base.models import BaseModel
from apps.scouts_groups.api.sections.models import ScoutsSection
from inuits.mixins import CreatedByMixin, AuditTimestampMixin
from inuits.models import OptionalDateField


logger = logging.getLogger(__name__)


class ScoutsCamp(CreatedByMixin, AuditTimestampMixin, BaseModel):
    """
    A model for a scout camp.
    """ 
    
    # @TODO model period, exceptions, test-driven
    name = models.TextField()
    start_date = OptionalDateField()
    end_date = OptionalDateField()
    sections = models.ManyToManyField(ScoutsSection)

    def clean(self):
        if not self.name:
            raise ValidationError(
                "A ScoutsCamp must have a name")
        # This can't be done, because there is no ScoutsCamp instance yet.
        # Validate the presence of at least 1 ScoutsSection in uuid in the
        # serializer's validate method.
        #if not self.sections or len(self.sections) == 0:
        #    raise ValidationError(
        #        "A ScoutsCamp must have at least 1 ScoutsSection attached")


