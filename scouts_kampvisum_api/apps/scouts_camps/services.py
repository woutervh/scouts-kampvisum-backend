import uuid
from .models import ScoutsCamp


class ScoutsCampService():
    def camp_create(self, *, name, start_date, end_date) -> ScoutsCamp:
        '''
        Saves a ScoutsCamp object to the DB.
        '''
        
        camp = ScoutsCamp(
            name=name,
            start_date=start_date,
            end_date=end_date,
            uuid=uuid.uuid4()
            )
        
        camp.full_clean()
        camp.save()
        
        return camp
    
    def camp_update(self, *, camp: ScoutsCamp, **fields) -> ScoutsCamp:
        '''
        Updates an existing ScoutsCamp object in the DB.
        '''
        
        camp.name = fields.get('name', camp.name)
        camp.start_date = fields.get('start_date', camp.start_date)
        camp.end_date = fields.get('end_date', camp.end_date)
        
        camp.full_clean()
        camp.save()
        
        return camp

