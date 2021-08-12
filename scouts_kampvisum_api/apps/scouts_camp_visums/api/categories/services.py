from .models import ScoutsCampVisumCategory, ScoutsCampVisumSubCategory


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


class ScoutsCampVisumSubCategoryService():
    
    def create(
            self, *,
            name: str,
            category: ScoutsCampVisumCategory) -> ScoutsCampVisumSubCategory:
        """
        Saves a ScoutsCampVisumSubCategory object to the DB.
        """
        
        instance = ScoutsCampVisumSubCategory(
            category=category,
            name=name,
        )
        
        instance.full_clean()
        instance.save()
        
        return instance
    
    def update(
            self,
            *,
            instance: ScoutsCampVisumSubCategory,
            **fields) -> ScoutsCampVisumSubCategory:
        """
        Updates an existing ScoutsCampVisumSubCategory object in the DB.
        """
        
        instance.category = fields.get('category', instance.category)
        instance.name = fields.get('name', instance.name)
        
        instance.full_clean()
        instance.save()
        
        return instance

