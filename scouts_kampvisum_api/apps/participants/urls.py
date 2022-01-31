from django.urls import path
from rest_framework import routers

from apps.participants.views import (
    ParticipantViewSet,
)

urlpatterns = [
    path(
        "participants/members/",
        ParticipantViewSet.as_view({"get": "list_scouts_members"}),
    ),
]


router = routers.SimpleRouter()

router.register(r"participants", ParticipantViewSet, "participants")

urlpatterns += router.urls
