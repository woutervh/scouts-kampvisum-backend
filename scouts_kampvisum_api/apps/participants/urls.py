from rest_framework import routers

from apps.participants.views import (
    ParticipantViewSet,
)

router = routers.SimpleRouter()

router.register(r"participants", ParticipantViewSet, "members")

urlpatterns = router.urls
