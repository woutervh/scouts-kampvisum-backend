class LinkedCheckEndpointFactory:
    @staticmethod
    def get_endpoint(endpoint: str):
        return "checks/{}".format(endpoint)


from django.urls import path
from rest_framework import routers

from apps.visums.views import (
    CampTypeViewSet,
    CategoryViewSet,
    SubCategoryViewSet,
    CategorySetViewSet,
    CampVisumViewSet,
    LinkedCheckViewSet,
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
location_unlink = LinkedCheckViewSet.as_view(
    {
        "delete": "unlink_location",
    }
)
camp_location_check = LinkedCheckViewSet.as_view(
    {
        "get": "retrieve_camp_location_check",
        "patch": "partial_update_camp_location_check",
    }
)
camp_location_unlink = LinkedCheckViewSet.as_view(
    {
        "delete": "unlink_camp_location",
    }
)
participant_check = LinkedCheckViewSet.as_view(
    {
        "get": "retrieve_participant_check",
        "patch": "partial_update_participant_check",
    }
)
participant_check_unlink = LinkedCheckViewSet.as_view(
    {
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
        "checks/location/<uuid:check_id>/<uuid:location_id>",
        location_unlink,
        name="location_unlink",
    ),
    path(
        "checks/camp_location/<uuid:check_id>",
        camp_location_check,
        name="camp_location_check",
    ),
    path(
        "checks/camp_location/<uuid:check_id>/<uuid:camp_location_id>",
        camp_location_unlink,
        name="camp_location_unlink",
    ),
    path(
        "checks/participant/<uuid:check_id>",
        participant_check,
        name="participant_check",
    ),
    path(
        "checks/participant/<uuid:check_id>/<uuid:participant_id>",
        participant_check_unlink,
        name="participant_check_unlink",
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
]


router = routers.SimpleRouter()

router.register("camp_types", CampTypeViewSet, "camp_types")
router.register(r"categories", CategoryViewSet, "categories")
router.register(r"sub_categories", SubCategoryViewSet, "sub_categories")
router.register(r"category_sets", CategorySetViewSet, "category_sets")
router.register(r"visums", CampVisumViewSet, "visums")
router.register(r"checks", LinkedCheckViewSet, "checks")

urlpatterns += router.urls
