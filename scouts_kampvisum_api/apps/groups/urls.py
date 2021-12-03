from rest_framework import routers

from .api.views import (
    SectionViewSet,
    SectionNameViewSet,
    GroupViewSet,
)


router = routers.SimpleRouter()

router.register(r"groups", GroupViewSet, "groups")
router.register(r"sections", SectionViewSet, "sections")
router.register(r"section_names", SectionNameViewSet, "section_names")

urlpatterns = router.urls
