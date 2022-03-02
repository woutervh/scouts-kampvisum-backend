from rest_framework import routers

from apps.groups.views import (
    ScoutsSectionViewSet,
    ScoutsSectionNameViewSet,
)


router = routers.SimpleRouter()

router.register(r"sections", ScoutsSectionViewSet, "sections")
router.register(r"section_names", ScoutsSectionNameViewSet, "section_names")

urlpatterns = router.urls
