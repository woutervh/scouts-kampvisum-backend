from rest_framework import routers

from .api.sections.views import ScoutsSectionViewSet, ScoutsSectionNameViewSet
from .api.groups.views import ScoutsGroupViewSet


router = routers.SimpleRouter()

router.register(r'groups', ScoutsGroupViewSet, 'groups')
router.register(r'sections', ScoutsSectionViewSet, 'sections')
router.register(r'section_names', ScoutsSectionNameViewSet, 'section_names')

urlpatterns = router.urls