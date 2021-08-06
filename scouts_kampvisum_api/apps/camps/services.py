'''
Created on Jul 27, 2021

@author: boro
'''
import uuid
from .models import Camp


class CampService():
    def camp_create(self, *, name, start_date, end_date) -> Camp:
        '''
        Saves a Camp object to the DB.
        '''
        
        camp = Camp(
            name=name,
            start_date=start_date,
            end_date=end_date,
            uuid=uuid.uuid4()
            )
        
        camp.full_clean()
        camp.save()
        
        return camp
    
    def camp_update(self, *, camp: Camp, **fields) -> Camp:
        '''
        Updates an existing Camp object in the DB.
        '''
        
        camp.name = fields.get('name', camp.name)
        camp.start_date = fields.get('start_date', camp.start_date)
        camp.end_date = fields.get('end_date', camp.end_date)
        
        camp.full_clean()
        camp.save()
        
        return camp

