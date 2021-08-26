from ..models import (
    CampVisumCategory,
    CampVisumSubCategory
)


class CampVisumSubCategoryService():
    
    def create(
            self, *,
            name: str,
            category: CampVisumCategory) -> CampVisumSubCategory:
        """
        Saves a CampVisumSubCategory object to the DB.
        """
        
        instance = CampVisumSubCategory(
            category=category,
            name=name,
        )
        
        instance.full_clean()
        instance.save()
        
        return instance
    
    def update(
            self,
            *,
            instance: CampVisumSubCategory,
            **fields) -> CampVisumSubCategory:
        """
        Updates an existing CampVisumSubCategory object in the DB.
        """
        
        instance.category = fields.get('category', instance.category)
        instance.name = fields.get('name', instance.name)
        
        instance.full_clean()
        instance.save()
        
        return instance

