from rest_framework import routers
from .api.categories.viewsets import ScoutsCampVisumCategoryViewSet
from .api.sub_categories.viewsets import ScoutsCampVisumSubCategoryViewSet


router = routers.SimpleRouter()

router.register(
    r'categories', ScoutsCampVisumCategoryViewSet, 'categories')
router.register(
    r'sub_categories', ScoutsCampVisumSubCategoryViewSet, 'sub_categories')

urlpatterns = router.urls

