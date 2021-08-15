from rest_framework import routers

from .api.sections.viewsets import ScoutsSectionNameViewSet
from .api.groups.viewsets import ScoutsGroupViewSet, GroupAdminGroupViewSet


router = routers.SimpleRouter()

router.register(r'groupadmin', GroupAdminGroupViewSet, 'groupadmin')
router.register(r'groups', ScoutsGroupViewSet, 'groups')
router.register(r'sections', ScoutsSectionNameViewSet, 'sections')

urlpatterns = router.urls