from django.utils import timezone

from apps.deadlines.models import DeadlineDate

class DeadlineDateService:
    
    def create_deadline_date(self, request, **fields) -> DeadlineDate:
        instance = DeadlineDate()
        
        instance.date_day = fields.get("date_day", None)
        instance.date_month = fields.get("date_month", None)
        instance.date_year = fields.get("date_year", None)
        instance.created_by = request.user
        
        instance.full_clean()
        instance.save()
        
        return instance
    
    
    
    def update_deadline_date(self, request, instance: DeadlineDate, **fields) -> DeadlineDate:
        instance = DeadlineDate()
        
        instance.date_day = fields.get("date_day", instance.date_day)
        instance.date_month = fields.get("date_month", instance.date_month)
        instance.date_year = fields.get("date_year", instance.date_year)
        instance.updated_by = request.user
        instance.updated_on = timezone.now()
        
        instance.full_clean()
        instance.save()
        
        return instance