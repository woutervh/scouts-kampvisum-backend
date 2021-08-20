from rest_framework import routers
from .views import ScoutsCampViewSet
from .views_api import ScoutsCampAPIViewSet


router = routers.SimpleRouter()

router.register(r'camps', ScoutsCampAPIViewSet, 'camp')
router.register(r'debug/camps', ScoutsCampViewSet, 'debug_camp')

urlpatterns = router.urls

