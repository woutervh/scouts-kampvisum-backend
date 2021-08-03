import uuid
from django.db import models
from django.core.exceptions import ValidationError


class Camp(models.Model):
    '''A model for a scout camp.''' 
    id = models.AutoField(db_column='campid', primary_key=True)
    name = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4(), editable=False)
    
    class Meta:
        db_table = 'camps'
        managed = True

    def clean(self):
        if not self.start_date or not self.end_date:
            raise ValidationError('Start and end dates need to be known')

