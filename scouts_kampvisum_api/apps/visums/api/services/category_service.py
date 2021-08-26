from ..models import CampVisumCategory


class CampVisumCategoryService():
    
    def create(
            self, *, name: str) -> CampVisumCategory:
        """
        Saves a CampVisumCategory object to the DB.
        """
        
        instance = CampVisumCategory(
            name=name,
        )
        
        instance.full_clean()
        instance.save()
        
        return instance
    
    def update(
            self,
            *,
            instance: CampVisumCategory,
            **fields) -> CampVisumCategory:
        """
        Updates an existing CampVisumCategory object in the DB.
        """
        
        instance.name = fields.get('name', instance.name)
        
        instance.full_clean()
        instance.save()
        
        return instance

