from rest_framework import routers
from .categories.viewsets import ScoutsCampVisumCategoryViewSet
from .categories.viewsets import ScoutsCampVisumSubCategoryViewSet


router = routers.SimpleRouter()

router.register(
    r'categories', ScoutsCampVisumCategoryViewSet, 'categories')
router.register(
    r'sub_categories', ScoutsCampVisumSubCategoryViewSet, 'sub_categories')

urlpatterns = router.urls

