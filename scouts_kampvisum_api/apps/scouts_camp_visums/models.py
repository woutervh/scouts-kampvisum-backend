
from django.db import models
from ..base.models import BaseModel

class ScoutsCampCheckCategory(BaseModel):
    
    name = models.CharField(
        max_length=128)
    
    def clean(self):
        pass


class ScoutsCampCheckSubCategory(BaseModel):
    
    def clean(self):
        pass


class ScoutsCampCheck(BaseModel):
    
    def clean(self):
        pass


