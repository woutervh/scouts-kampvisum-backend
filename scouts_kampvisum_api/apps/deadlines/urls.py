from django.urls import path
from rest_framework import routers

from apps.deadlines.views import LinkedDeadlineViewSet

visum = LinkedDeadlineViewSet.as_view({"get": "list_for_visum"})
flags = LinkedDeadlineViewSet.as_view(
    {
        "get": "partial_update_linked_deadline_flag",
        "patch": "partial_update_linked_deadline_flag",
    }
)

urlpatterns = [
    path("deadlines/visum/<uuid:visum_id>", visum, name="visum"),
    path(
        "deadlines/flags/<uuid:linked_deadline_id>/<uuid:linked_deadline_flag_id>",
        flags,
        name="flags",
    ),
]


router = routers.SimpleRouter()

router.register(r"deadlines", LinkedDeadlineViewSet, "deadlines")

urlpatterns += router.urls
