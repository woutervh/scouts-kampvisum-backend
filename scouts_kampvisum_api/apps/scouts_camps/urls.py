from rest_framework import routers
from .views import ScoutsCampViewSet


router = routers.SimpleRouter()

router.register(r'camps', ScoutsCampViewSet, 'camp')

urlpatterns = router.urls

