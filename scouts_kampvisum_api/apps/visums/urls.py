from rest_framework import routers

from .api.views import (
    CampVisumCategoryViewSet,
    CampVisumSubCategoryViewSet,
    CampVisumCategorySetViewSet,
    CampVisumAPIViewSet
)


router = routers.SimpleRouter()

router.register(
    r'categories', CampVisumCategoryViewSet, 'categories')
router.register(
    r'sub_categories', CampVisumSubCategoryViewSet, 'sub_categories')
router.register(
    r'category_sets', CampVisumCategorySetViewSet, 'category_sets')
router.register(
    r'visums', CampVisumAPIViewSet, 'visums')

urlpatterns = router.urls
