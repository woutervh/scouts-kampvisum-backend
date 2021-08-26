from rest_framework import routers

from .api.views import (
    CampVisumCategoryViewSet,
    CampVisumSubCategoryViewSet,
    CampVisumConcernViewSet,
    CampVisumCategorySetViewSet,
)


router = routers.SimpleRouter()

router.register(
    r'categories', CampVisumCategoryViewSet, 'categories')
router.register(
    r'sub_categories', CampVisumSubCategoryViewSet, 'sub_categories')
router.register(
    r'category_sets', CampVisumCategorySetViewSet, 'category_sets')

urlpatterns = router.urls
