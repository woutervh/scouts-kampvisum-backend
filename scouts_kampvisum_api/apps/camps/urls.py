from rest_framework import routers
from .views import CampViewSet, CampYearViewSet, CampTypeViewSet


router = routers.SimpleRouter()

router.register(r"camps", CampViewSet, "camp")
router.register(r"camp_years", CampYearViewSet, "camp")
router.register(r"camp_types", CampTypeViewSet, "camp_types")

urlpatterns = router.urls
