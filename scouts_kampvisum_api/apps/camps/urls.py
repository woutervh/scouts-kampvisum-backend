from rest_framework import routers
from .views import CampViewSet, CampYearViewSet


router = routers.SimpleRouter()

router.register(r"camps", CampViewSet, "camp")
router.register(r"camp_years", CampYearViewSet, "camp")

urlpatterns = router.urls
