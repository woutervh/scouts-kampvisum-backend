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
    CampVisumLocationViewSet,
    CampVisumEngagementViewSet,
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

feedback = CampVisumApprovalViewSet.as_view({"patch": "partial_update_feedback"})
approval = CampVisumApprovalViewSet.as_view({"patch": "partial_update_approval"})
global_approval = CampVisumApprovalViewSet.as_view({"patch": "global_update_approval"})
global_disapproval = CampVisumApprovalViewSet.as_view(
    {"patch": "global_update_disapproval"}
)
notes = CampVisumApprovalViewSet.as_view({"patch": "partial_update_dc_notes"})
handle_feedback = CampVisumApprovalViewSet.as_view({"patch": "handle_feedback"})
global_handle_feedback = CampVisumApprovalViewSet.as_view(
    {"patch": "global_handle_feedback"}
)
dates_leaders = CampVisumViewSet.as_view(
    {"get": "dates_leaders"}
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
    path("visums/<uuid:linked_sub_category_id>/feedback", feedback, name="feedback"),
    path("visums/<uuid:linked_sub_category_id>/approval", approval, name="approval"),
    path(
        "visums/<uuid:visum_id>/global_approval",
        global_approval,
        name="global_approval",
    ),
    path(
        "visums/<uuid:visum_id>/global_disapproval",
        global_disapproval,
        name="global_disapproval",
    ),
    path("visums/<uuid:visum_id>/notes", notes, name="notes"),
    path(
        "visums/<uuid:linked_sub_category_id>/handle_feedback",
        handle_feedback,
        name="handle_feedback",
    ),
    path(
        "visums/<uuid:visum_id>/global_handle_feedback",
        global_handle_feedback,
        name="global_handle_feedback",
    ),
    path(
        "visums/<uuid:pk>/dates/leaders",
        dates_leaders,
        name="visums",
    ),
]


router = routers.SimpleRouter()

router.register(r"categories", CategoryViewSet, "categories")
router.register(r"sub_categories", SubCategoryViewSet, "sub_categories")
router.register(r"visums/engagement", CampVisumEngagementViewSet, "approvals")
router.register(r"visums/locations", CampVisumLocationViewSet, "visums_locations")
router.register(r"visums_categories", LinkedCategoryViewSet, "categories")
router.register(r"checks", LinkedCheckViewSet, "checks")
router.register(r"visums", CampVisumViewSet, "visums")

urlpatterns += router.urls
