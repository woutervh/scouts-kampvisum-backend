class LinkedCheckEndpointFactory:
    @staticmethod
    def get_endpoint(endpoint: str):
        return "checks/{}".format(endpoint)


from django.urls import path
from rest_framework import routers

from apps.deadlines.views import DeadlineViewSet

sub_category_list = DeadlineViewSet.as_view(
    {
        "post": "create_linked_sub_category_deadline",
        "get": "list_linked_sub_category_deadlines",
    }
)
sub_category = DeadlineViewSet.as_view(
    {
        "get": "retrieve_linked_sub_category_deadline",
        "patch": "partial_update_linked_sub_category_deadline",
    }
)
checks_list = DeadlineViewSet.as_view(
    {"post": "create_linked_check_deadline", "get": "list_linked_check_deadlines"}
)
checks = DeadlineViewSet.as_view(
    {
        "get": "retrieve_linked_check_deadline",
        "patch": "partial_update_linked_check_deadline",
    }
)
mixed_list = DeadlineViewSet.as_view(
    {"post": "create_mixed_deadline", "get": "list_mixed_deadlines"}
)
mixed = DeadlineViewSet.as_view(
    {
        "get": "retrieve_mixed_deadline",
        "patch": "partial_update_mixed_deadline",
    }
)
visum = DeadlineViewSet.as_view({"get": "list_for_visum"})
flags = DeadlineViewSet.as_view(
    {
        "get": "partial_update_deadline_flag",
        "patch": "partial_update_deadline_flag",
    }
)

urlpatterns = [
    path(
        "deadlines/sub_category/",
        sub_category_list,
        name="sub_category_list",
    ),
    path(
        "deadlines/sub_category/<uuid:deadline_id>",
        sub_category,
        name="sub_category",
    ),
    path(
        "deadlines/checks/",
        checks_list,
        name="checks_list",
    ),
    path(
        "deadlines/checks/<uuid:deadline_id>",
        checks,
        name="checks",
    ),
    path(
        "deadlines/mixed/",
        mixed_list,
        name="mixed_list",
    ),
    path(
        "deadlines/mixed/<uuid:deadline_id>",
        mixed,
        name="mixed",
    ),
    path("deadlines/visum/<uuid:visum_id>", visum, name="visum"),
    path("deadlines/flags/<uuid:deadline_flag_id>", flags, name="flags"),
]


router = routers.SimpleRouter()

router.register(r"deadlines", DeadlineViewSet, "deadlines")

urlpatterns += router.urls
