from rest_framework import routers
from .viewsets import ScoutsCampViewSet


router = routers.SimpleRouter()

router.register(r'camps', ScoutsCampViewSet, 'camp')

urlpatterns = router.urls

