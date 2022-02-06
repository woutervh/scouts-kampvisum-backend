import datetime

from scouts_auth.inuits.models import AuditedBaseModel
from scouts_auth.inuits.models.fields import OptionalIntegerField

class DeadlineDate(AuditedBaseModel):
    
    date_day = OptionalIntegerField()
    date_month = OptionalIntegerField()
    date_year = OptionalIntegerField()
    
    def to_date(self) -> datetime.date:
        day = self.day if self.day else 1
        month = self.month if self.month else 1
        year = self.year if self.year else datetime.datetime.now().date().year
        
        return datetime.date(year, month, day)
    