from .models import ScoutsSectionName


class ScoutsSectionNameService():
    def name_create(self, *, name) -> ScoutsSectionName:
        """
        Saves a ScoutsTroopName object to the DB.
        """
        
        instance = ScoutsSectionName(
            name = name,
        )
        
        instance.full_clean()
        instance.save()
        
        return instance
    
    def name_update(
            self, *,
            instance: ScoutsSectionName, **fields) -> ScoutsSectionName:
        """
        Updates an existing ScoutsSectionName object in the DB.
        """
        
        instance.name = fields.get('name', instance.name)
        
        instance.full_clean()
        instance.save()
        
        return instance

