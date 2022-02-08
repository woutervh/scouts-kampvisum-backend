class LinkedCheckEndpointFactory:
    @staticmethod
    def get_endpoint(endpoint: str):
        return "checks/{}".format(endpoint)


from django.urls import path
from rest_framework import routers

from apps.deadlines.views import DeadlineViewSet

sub_category_list = DeadlineViewSet.as_view(
    {"post": "create_sub_category_deadline", "get": "list_sub_category_deadlines"}
)
sub_category = DeadlineViewSet.as_view(
    {"get": "retrieve_sub_category_deadline", "patch": "partial_update_sub_category_deadline"}
)
checks_list = DeadlineViewSet.as_view(
    {"post": "create_check_deadline", "get": "list_check_deadlines"}
)
checks = DeadlineViewSet.as_view(
    {"get": "retrieve_check_deadline", "patch": "partial_update_check_deadline"}
)
deadline_dependent = DeadlineViewSet.as_view(
    {"get": "retrieve_deadline_dependent_deadline", "patch": "partial_update_deadline_dependent_deadline"}
)
visum = DeadlineViewSet.as_view(
    {"get": "list_for_visum"}
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
        "deadlines/visum/<uuid:visum_id>",
        visum,
        name="visum"
    )
]


router = routers.SimpleRouter()

router.register(r"deadlines", DeadlineViewSet, "deadlines")

urlpatterns += router.urls
