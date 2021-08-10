from rest_framework import routers
from .viewsets import CampViewSet


router = routers.SimpleRouter()

router.register(r'camps', CampViewSet, 'camp')

urlpatterns = router.urls

