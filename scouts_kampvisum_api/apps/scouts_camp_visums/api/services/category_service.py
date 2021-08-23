from ..models import ScoutsCampVisumCategory


class ScoutsCampVisumCategoryService():
    
    def create(
            self, *, name: str) -> ScoutsCampVisumCategory:
        """
        Saves a ScoutsCampVisumCategory object to the DB.
        """
        
        instance = ScoutsCampVisumCategory(
            name=name,
        )
        
        instance.full_clean()
        instance.save()
        
        return instance
    
    def update(
            self,
            *,
            instance: ScoutsCampVisumCategory,
            **fields) -> ScoutsCampVisumCategory:
        """
        Updates an existing ScoutsCampVisumCategory object in the DB.
        """
        
        instance.name = fields.get('name', instance.name)
        
        instance.full_clean()
        instance.save()
        
        return instance

