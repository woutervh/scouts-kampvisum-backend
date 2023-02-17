from rest_framework import routers

from apps.groups.views import ScoutsSectionViewSet


router = routers.SimpleRouter()

router.register(r"sections", ScoutsSectionViewSet, "sections")

urlpatterns = router.urls
