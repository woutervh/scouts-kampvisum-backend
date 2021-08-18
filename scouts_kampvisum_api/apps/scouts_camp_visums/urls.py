from rest_framework import routers
from .api.categories.views import ScoutsCampVisumCategoryViewSet
from .api.sub_categories.views import ScoutsCampVisumSubCategoryViewSet


router = routers.SimpleRouter()

router.register(
    r'categories', ScoutsCampVisumCategoryViewSet, 'categories')
router.register(
    r'sub_categories', ScoutsCampVisumSubCategoryViewSet, 'sub_categories')

urlpatterns = router.urls

