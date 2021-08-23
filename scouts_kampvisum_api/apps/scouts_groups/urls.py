from rest_framework import routers

from .api.views import (
    ScoutsSectionViewSet,
    ScoutsSectionNameViewSet,
    ScoutsGroupViewSet,
)


router = routers.SimpleRouter()

router.register(r'groups', ScoutsGroupViewSet, 'groups')
router.register(r'sections', ScoutsSectionViewSet, 'sections')
router.register(r'section_names', ScoutsSectionNameViewSet, 'section_names')

urlpatterns = router.urls