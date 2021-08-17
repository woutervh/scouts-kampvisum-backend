from django.db import models
from django.core.exceptions import ValidationError

from ..base.models import BaseModel


class ScoutsCamp(BaseModel):
    """
    A model for a scout camp.
    """ 
    
    name = models.TextField()
    
    # @TODO model period, exceptions, test-driven
    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        if not self.start_date or not self.end_date:
            raise ValidationError("Start and end dates need to be known")


