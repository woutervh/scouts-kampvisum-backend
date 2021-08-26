from rest_framework import routers
from .views import CampViewSet
from .views_api import CampAPIViewSet


router = routers.SimpleRouter()

router.register(r'camps', CampAPIViewSet, 'camp')
router.register(r'debug/camps', CampViewSet, 'debug_camp')

urlpatterns = router.urls
