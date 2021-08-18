from rest_framework import routers

from .api.sections.views import ScoutsSectionNameViewSet
from .api.groups.views import ScoutsGroupViewSet


router = routers.SimpleRouter()

router.register(r'groups', ScoutsGroupViewSet, 'groups')
router.register(r'sections', ScoutsSectionNameViewSet, 'sections')

urlpatterns = router.urls