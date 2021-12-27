from django.urls import path
from rest_framework import routers

from scouts_auth.groupadmin.views import (
    ScoutsSectionViewSet,
    ScoutsSectionNameViewSet,
)


router = routers.SimpleRouter()

router.register(r"sections", ScoutsSectionViewSet, "sections")
router.register(r"section_names", ScoutsSectionNameViewSet, "section_names")

urlpatterns = router.urls
