import uuid
from django.db import models
from safedelete.models import SafeDeleteModel
from safedelete.models import HARD_DELETE, SOFT_DELETE

from scouts_auth.models import ScoutsGroup

# FIXTURE: scouts_troop_names
# Taken from https://nl.wikipedia.org/wiki/Tak_(scouting)
class ScoutsTroopName(SafeDeleteModel):
    """
    A simple string model to represent a Scouts Troop name.
    
    This can be used to provide a consistent list of troop names to
    choose from.
    """
    
    # Setting to HARD_DELETE because a troop name may be incorrect
    _safedelete_policy = HARD_DELETE
    
    id = models.AutoField(
        primary_key=True, editable=False)
    uuid = models.UUIDField(
        primary_key=False, default=uuid.uuid4(), editable=False, unique=True)
    name = models.CharField(
        max_length=128)
    
    def clean(self):
        pass


class ScoutsTroop(SafeDeleteModel):
    """
    A model for Scouts Troops, linking them to their Scouts Group and name.
    """
    
    _safedelete_policy = SOFT_DELETE
    
    group = models.ForeignKey(ScoutsGroup, on_delete = models.CASCADE)
    name = models.ForeignKey(ScoutsTroopName, on_delete = models.DO_NOTHING)
    
    def clean(self):
        pass

