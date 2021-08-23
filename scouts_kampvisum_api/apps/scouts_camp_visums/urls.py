from rest_framework import routers
from .api.views import (
    ScoutsCampVisumCategoryViewSet,
    ScoutsCampVisumSubCategoryViewSet,
    ScoutsCampVisumCheckViewSet
)


router = routers.SimpleRouter()

router.register(
    r'categories', ScoutsCampVisumCategoryViewSet, 'categories')
router.register(
    r'sub_categories', ScoutsCampVisumSubCategoryViewSet, 'sub_categories')

urlpatterns = router.urls

