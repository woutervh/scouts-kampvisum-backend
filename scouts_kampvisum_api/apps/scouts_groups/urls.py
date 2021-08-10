from rest_framework import routers
from .viewsets import ScoutsTroopNameViewSet


router = routers.SimpleRouter()

router.register(r'troops', ScoutsTroopNameViewSet, 'troop')

urlpatterns = router.urls