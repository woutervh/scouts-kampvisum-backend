class LinkedCheckEndpointFactory:
    @staticmethod
    def get_endpoint(endpoint: str):
        return "checks/{}".format(endpoint)


from django.urls import path
from rest_framework import routers

from apps.visums.views import (
    CategoryViewSet,
    SubCategoryViewSet,
    CampVisumViewSet,
    CampVisumApprovalViewSet,
    LinkedCheckViewSet,
    LinkedCategoryViewSet,
)

simple_check = LinkedCheckViewSet.as_view(
    {"get": "retrieve_simple_check", "patch": "partial_update_simple_check"}
)
date_check = LinkedCheckViewSet.as_view(
    {"get": "retrieve_date_check", "patch": "partial_update_date_check"}
)
duration_check = LinkedCheckViewSet.as_view(
    {"get": "retrieve_duration_check", "patch": "partial_update_duration_check"}
)
location_check = LinkedCheckViewSet.as_view(
    {"get": "retrieve_location_check", "patch": "partial_update_location_check"}
)
camp_location_check = LinkedCheckViewSet.as_view(
    {
        "get": "retrieve_camp_location_check",
        "patch": "partial_update_camp_location_check",
    }
)
participant_check = LinkedCheckViewSet.as_view(
    {
        "get": "retrieve_participant_check",
        "patch": "partial_update_participant_check",
    }
)
participant_check_participant = LinkedCheckViewSet.as_view(
    {
        "patch": "toggle_participant_payment_status",
        "delete": "unlink_participant",
    }
)
file_upload_check = LinkedCheckViewSet.as_view(
    {
        "get": "retrieve_file_upload_check",
        "patch": "partial_update_file_upload_check",
    }
)
file_upload_check_unlink = LinkedCheckViewSet.as_view(
    {
        "delete": "unlink_file",
    }
)
comment_check = LinkedCheckViewSet.as_view(
    {"get": "retrieve_comment_check", "patch": "partial_update_comment_check"}
)
number_check = LinkedCheckViewSet.as_view(
    {"get": "retrieve_number_check", "patch": "partial_update_number_check"}
)

urlpatterns = [
    path("checks/simple/<uuid:check_id>", simple_check, name="simple_check"),
    path("checks/date/<uuid:check_id>", date_check, name="date_check"),
    path(
        "checks/duration/<uuid:check_id>",
        duration_check,
        name="duration_check",
    ),
    path(
        "checks/location/<uuid:check_id>",
        location_check,
        name="location_check",
    ),
    path(
        "checks/camp_location/<uuid:check_id>",
        camp_location_check,
        name="camp_location_check",
    ),
    path(
        "checks/participant/<uuid:check_id>",
        participant_check,
        name="participant_check",
    ),
    path(
        "checks/participant/<uuid:check_id>/<uuid:visum_participant_id>",
        participant_check_participant,
        name="participant_check_participant",
    ),
    path(
        "checks/file/<uuid:check_id>",
        file_upload_check,
        name="file_upload_check",
    ),
    path(
        "checks/file/<uuid:check_id>/<uuid:persisted_file_id>",
        file_upload_check_unlink,
        name="file_upload_check_unlink",
    ),
    path(
        "checks/comment/<uuid:check_id>",
        comment_check,
        name="comment_check",
    ),
    path(
        "checks/number/<uuid:check_id>",
        number_check,
        name="number_check",
    ),
]


router = routers.SimpleRouter()

router.register(r"categories", CategoryViewSet, "categories")
router.register(r"sub_categories", SubCategoryViewSet, "sub_categories")
router.register(r"visums/approval", CampVisumApprovalViewSet, "approvals")
router.register(r"visums", CampVisumViewSet, "visums")
router.register(r"visums_categories", LinkedCategoryViewSet, "categories")
router.register(r"checks", LinkedCheckViewSet, "checks")

urlpatterns += router.urls
