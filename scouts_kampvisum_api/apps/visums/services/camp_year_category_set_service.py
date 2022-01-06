from apps.camps.models import CampYear
from apps.visums.models import CampYearCategorySet


class CampYearCategorySetService:
    def get_category_set(self, request, year: CampYear) -> CampYearCategorySet:
        return CampYearCategorySet.objects.get(camp_year=year)
