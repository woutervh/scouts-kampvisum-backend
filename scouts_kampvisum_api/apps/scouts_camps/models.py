from django.db import models
from django.core.exceptions import ValidationError

from apps.base.models import BaseModel
from apps.scouts_groups.api.sections.models import ScoutsSection


class ScoutsCamp(BaseModel):
    """
    A model for a scout camp.
    """ 
    
    # @TODO model period, exceptions, test-driven
    name = models.TextField()
    start_date = models.DateField(default=None)
    end_date = models.DateField(default=None)
    sections = models.ManyToManyField(ScoutsSection)

    def clean(self):
        if not self.start_date or not self.end_date:
            raise ValidationError("Start and end dates need to be known")


