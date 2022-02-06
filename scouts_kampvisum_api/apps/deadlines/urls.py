class LinkedCheckEndpointFactory:
    @staticmethod
    def get_endpoint(endpoint: str):
        return "checks/{}".format(endpoint)


from django.urls import path
from rest_framework import routers

from apps.deadlines.views import DeadlineViewSet

sub_category = DeadlineViewSet.as_view(
    {"get": "retrieve_sub_category_deadline", "patch": "partial_update_sub_category_deadline"}
)
sub_category_list = DeadlineViewSet.as_view(
    {"get": "list_sub_category_deadlines"}
)
check = DeadlineViewSet.as_view(
    {"get": "retrieve_check_deadline", "patch": "partial_update_check_deadline"}
)
deadline_dependent = DeadlineViewSet.as_view(
    {"get": "retrieve_deadline_dependent_deadline", "patch": "partial_update_deadline_dependent_deadline"}
)

urlpatterns = [
    path(
        "deadlines/sub_category",
        sub_category_list,
        name="sub_category_list",
    ),
    path(
        "deadlines/sub_category/<uuid:check_id>",
        sub_category,
        name="sub_category",
    ),
    path(
        "deadlines/check/<uuid:check_id>",
        check,
        name="check",
    ),
    path(
        "deadlines/deadline_dependent/<uuid:check_id>",
        deadline_dependent,
        name="deadline_dependent",
    ),
]


router = routers.SimpleRouter()

router.register(r"deadlines", DeadlineViewSet, "deadlines")

urlpatterns += router.urls
