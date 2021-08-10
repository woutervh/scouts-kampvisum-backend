from django.db import models
from safedelete.models import HARD_DELETE

from ..base.models import BaseModel, ScoutsGroup

# FIXTURE: scouts_troop_names
# Taken from https://nl.wikipedia.org/wiki/Tak_(scouting)
class ScoutsTroopName(BaseModel):
    """
    A simple string model to represent a Scouts Troop name.
    
    This can be used to provide a consistent list of troop names to
    choose from.
    """
    
    # Setting to HARD_DELETE because a troop name may be incorrect
    _safedelete_policy = HARD_DELETE
    
    name = models.CharField(
        max_length=128)
    
    def clean(self):
        pass


class ScoutsTroop(BaseModel):
    """
    A model for Scouts Troops, linking them to their Scouts Group and name.
    """
    
    group = models.ForeignKey(
        ScoutsGroup, on_delete = models.CASCADE)
    name = models.ForeignKey(
        ScoutsTroopName, on_delete = models.DO_NOTHING)
    
    def clean(self):
        pass

