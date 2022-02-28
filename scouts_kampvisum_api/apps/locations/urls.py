from django.urls import path
from rest_framework import routers

from apps.locations.views import (
    LocationViewSet,
)


router = routers.SimpleRouter()

router.register(r"locations", LocationViewSet, "locations")

urlpatterns = router.urls
