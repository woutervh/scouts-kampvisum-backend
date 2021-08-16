import uuid
from .models import ScoutsCamp


class ScoutsCampService():
    
    def camp_create(self, *, name, start_date, end_date) -> ScoutsCamp:
        """
        Saves a ScoutsCamp object to the DB.
        """
        
        camp = ScoutsCamp(
            name=name,
            start_date=start_date,
            end_date=end_date,
            uuid=uuid.uuid4()
            )
        
        camp.full_clean()
        camp.save()
        
        return camp
    
    def camp_update(self, *, instance: ScoutsCamp, **fields) -> ScoutsCamp:
        """
        Updates an existing ScoutsCamp object in the DB.
        """
        
        instance.name = fields.get('name', instance.name)
        instance.start_date = fields.get('start_date', instance.start_date)
        instance.end_date = fields.get('end_date', instance.end_date)
        
        instance.full_clean()
        instance.save()
        
        return instance

