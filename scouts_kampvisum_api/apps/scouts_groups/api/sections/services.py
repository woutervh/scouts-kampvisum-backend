'''
Created on Jul 27, 2021

@author: boro
'''
import uuid
from .models import ScoutsTroopName


class ScoutsTroopNameService():
    def name_create(self, *, name) -> ScoutsTroopName:
        '''
        Saves a ScoutsTroopName object to the DB.
        '''
        
        name = ScoutsTroopName(
            name = name,
            uuid = uuid.uuid4(),
        )
        
        name.full_clean()
        name.save()
        
        return name
    
    def name_update(self, *, name: ScoutsTroopName, **fields) -> ScoutsTroopName:
        '''
        Updates an existing ScoutsTroopName object in the DB.
        '''
        
        name.name = fields.get('name', name.name)
        
        name.full_clean()
        name.save()
        
        return name

