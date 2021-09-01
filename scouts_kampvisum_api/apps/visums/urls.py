from rest_framework import routers

from .api.views import (
    CategoryViewSet,
    SubCategoryViewSet,
    CategorySetViewSet,
    CampVisumAPIViewSet
)


router = routers.SimpleRouter()

router.register(
    r'categories', CategoryViewSet, 'categories')
router.register(
    r'sub_categories', SubCategoryViewSet, 'sub_categories')
router.register(
    r'category_sets', CategorySetViewSet, 'category_sets')
router.register(
    r'visums', CampVisumAPIViewSet, 'visums')

urlpatterns = router.urls
