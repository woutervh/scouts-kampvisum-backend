class LinkedCheckEndpointFactory:
    @staticmethod
    def get_endpoint(endpoint: str):
        return "checks/{}".format(endpoint)


from django.urls import path
from rest_framework import routers

from apps.deadlines.views import LinkedDeadlineViewSet

visum = LinkedDeadlineViewSet.as_view({"get": "list_for_visum"})
flags = LinkedDeadlineViewSet.as_view(
    {
        "get": "partial_update_deadline_flag",
        "patch": "partial_update_deadline_flag",
    }
)

urlpatterns = [
    path("deadlines/visum/<uuid:visum_id>", visum, name="visum"),
    path(
        "deadlines/flags/<uuid:deadline_id>/<uuid:deadline_flag_id>",
        flags,
        name="flags",
    ),
]


router = routers.SimpleRouter()

router.register(r"deadlines", LinkedDeadlineViewSet, "deadlines")

urlpatterns += router.urls
