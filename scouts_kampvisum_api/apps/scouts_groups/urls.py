from rest_framework import routers
from .api.sections.viewsets import ScoutsSectionNameViewSet


router = routers.SimpleRouter()

router.register(r'troops', ScoutsSectionNameViewSet, 'troop')

urlpatterns = router.urls