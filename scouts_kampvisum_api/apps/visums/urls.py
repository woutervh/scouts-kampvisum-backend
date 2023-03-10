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
from rest_framework import routers
from django.urls import path


urlpatterns = []

urlpatterns.append(path(
    "checks/simple/<uuid:check_id>",
    LinkedCheckViewSet.as_view({
        "get": "retrieve_simple_check",
        "patch": "partial_update_simple_check"
    }),
    name="simple_check",
))

urlpatterns.append(path(
    "checks/date/<uuid:check_id>",
    LinkedCheckViewSet.as_view({
        "get": "retrieve_date_check",
        "patch": "partial_update_date_check"
    }),
    name="date_check",
))

urlpatterns.append(path(
    "checks/duration/<uuid:check_id>",
    LinkedCheckViewSet.as_view({
        "get": "retrieve_duration_check",
        "patch": "partial_update_duration_check"
    }),
    name="duration_check",
))

urlpatterns.append(path(
    "checks/location/<uuid:check_id>",
    LinkedCheckViewSet.as_view({
        "get": "retrieve_location_check",
        "patch": "partial_update_location_check"
    }),
    name="location_check",
))

urlpatterns.append(path(
    "checks/camp_location/<uuid:check_id>",
    LinkedCheckViewSet.as_view({
        "get": "retrieve_camp_location_check",
        "patch": "partial_update_camp_location_check",
    }),
    name="camp_location_check",
))

urlpatterns.append(path(
    "checks/participant/<uuid:check_id>",
    LinkedCheckViewSet.as_view({
        "get": "retrieve_participant_check",
        "patch": "partial_update_participant_check",
    }),
    name="participant_check",
))

urlpatterns.append(path(
    "checks/participant/<uuid:check_id>/<uuid:visum_participant_id>",
    LinkedCheckViewSet.as_view({
        "patch": "toggle_participant_payment_status",
        "delete": "unlink_participant",
    }),
    name="participant_check_participant",
))

urlpatterns.append(path(
    "checks/file/<uuid:check_id>",
    LinkedCheckViewSet.as_view({
        "get": "retrieve_file_upload_check",
        "patch": "partial_update_file_upload_check",
    }),
    name="file_upload_check",
))

urlpatterns.append(path(
    "checks/file/<uuid:check_id>/<uuid:persisted_file_id>",
    LinkedCheckViewSet.as_view({
        "delete": "unlink_file",
    }),
    name="file_upload_check_unlink",
))

urlpatterns.append(path(
    "checks/comment/<uuid:check_id>",
    LinkedCheckViewSet.as_view({
        "get": "retrieve_comment_check",
        "patch": "partial_update_comment_check"
    }),
    name="comment_check",
))

urlpatterns.append(path(
    "checks/number/<uuid:check_id>",
    LinkedCheckViewSet.as_view({
        "get": "retrieve_number_check",
        "patch": "partial_update_number_check"
    }),
    name="number_check",
))

urlpatterns.append(path(
    "visums/<uuid:linked_sub_category_id>/feedback",
    CampVisumApprovalViewSet.as_view({
        "patch": "partial_update_feedback"
    }),
    name="feedback",
))

urlpatterns.append(path(
    "visums/<uuid:linked_sub_category_id>/approval",
    CampVisumApprovalViewSet.as_view({
        "patch": "partial_update_approval"
    }),
    name="approval",
))

urlpatterns.append(path(
    "visums/<uuid:visum_id>/global_approval",
    CampVisumApprovalViewSet.as_view({
        "patch": "global_update_approval"
    }),
    name="global_approval",
))

urlpatterns.append(path(
    "visums/<uuid:visum_id>/global_disapproval",
    CampVisumApprovalViewSet.as_view({
        "patch": "global_update_disapproval"
    }),
    name="global_disapproval",
))

urlpatterns.append(path(
    "visums/<uuid:visum_id>/notes",
    CampVisumApprovalViewSet.as_view({
        "patch": "partial_update_dc_notes"
    }),
    name="notes",
))

urlpatterns.append(path(
    "visums/<uuid:linked_sub_category_id>/handle_feedback",
    CampVisumApprovalViewSet.as_view({
        "patch": "handle_feedback"
    }),
    name="handle_feedback",
))

urlpatterns.append(path(
    "visums/<uuid:visum_id>/global_handle_feedback",
    CampVisumApprovalViewSet.as_view({
        "patch": "global_handle_feedback"
    }),
    name="global_handle_feedback",
))

urlpatterns.append(path(
    "visums/<uuid:pk>/dates/leaders",
    CampVisumViewSet.as_view({
        "get": "dates_leaders"
    }),
    name="visums",
))

urlpatterns.append(path(
    "visums/all",
    CampVisumViewSet.as_view({
        "get": "list_all"
    }),
    name="visums",
))


router = routers.SimpleRouter()

router.register(r"categories", CategoryViewSet, "categories")
router.register(r"sub_categories", SubCategoryViewSet, "sub_categories")
router.register(r"visums/engagement", CampVisumEngagementViewSet, "approvals")
router.register(r"visums/locations",
                CampVisumLocationViewSet, "visums_locations")
router.register(r"visums_categories", LinkedCategoryViewSet, "categories")
router.register(r"checks", LinkedCheckViewSet, "checks")
router.register(r"visums", CampVisumViewSet, "visums")

urlpatterns += router.urls
