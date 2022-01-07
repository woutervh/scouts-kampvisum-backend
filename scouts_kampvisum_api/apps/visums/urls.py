class LinkedCheckEndpointFactory:
    @staticmethod
    def get_endpoint(endpoint: str):
        return "checks/{}".format(endpoint)


from rest_framework import routers

from apps.visums.views import (
    CategoryViewSet,
    SubCategoryViewSet,
    CategorySetViewSet,
    CampVisumViewSet,
    LinkedCheckViewSet,
)


router = routers.SimpleRouter()

router.register(r"categories", CategoryViewSet, "categories")
router.register(r"sub_categories", SubCategoryViewSet, "sub_categories")
router.register(r"category_sets", CategorySetViewSet, "category_sets")
router.register(r"visums", CampVisumViewSet, "visums")
router.register(r"checks", LinkedCheckViewSet, "checks")

urlpatterns = router.urls
