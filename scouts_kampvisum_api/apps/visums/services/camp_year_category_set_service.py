from apps.camps.models import CampYear
from apps.camps.services import CampYearService

from apps.visums.models import CampYearCategorySet


class CampYearCategorySetService:

    camp_year_service = CampYearService()

    def get_category_set(self, request, year: CampYear) -> CampYearCategorySet:
        try:
            return CampYearCategorySet.objects.get(camp_year=year)
        except:
            return None

    def get_category_set_for_current_year(self) -> CampYearCategorySet:
        return self.get_category_set(
            None, year=self.camp_year_service.get_or_create_current_camp_year()
        )

    def get_or_create_category_set_for_current_year(self) -> CampYearCategorySet:
        current = self.get_category_set_for_current_year()
        if not current:
            current = CampYearCategorySet()

            current.camp_year = self.camp_year_service.get_or_create_current_camp_year()

            current.full_clean()
            current.save()

        return current
