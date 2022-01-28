class LinkedCheckEndpointFactory:
    @staticmethod
    def get_endpoint(endpoint: str):
        return "checks/{}".format(endpoint)


from django.urls import path
from rest_framework import routers

from apps.visums.views import (
    CategoryViewSet,
    SubCategoryViewSet,
    CategorySetViewSet,
    CampVisumViewSet,
    LinkedCheckViewSet,
)

# patch_simple_check = LinkedCheckViewSet.as_view(
#     {"patch": "partial_update_simple_check"}
# )
# patch_date_check = LinkedCheckViewSet.as_view({"patch": "partial_update_date_check"})
# patch_duration_check = LinkedCheckViewSet.as_view(
#     {"patch": "partial_update_duration_check"}
# )
# patch_location_check = LinkedCheckViewSet.as_view(
#     {"patch": "partial_update_location_check"}
# )
# patch_camp_location_check = LinkedCheckViewSet.as_view(
#     {"patch": "partial_update_camp_location_check"}
# )
# patch_participant_check = LinkedCheckViewSet.as_view(
#     {"patch": "partial_update_participant_check"}
# )
# patch_file_upload_check = LinkedCheckViewSet.as_view(
#     {"patch": "partial_update_file_upload_check"}
# )
# patch_comment_check = LinkedCheckViewSet.as_view(
#     {"patch": "partial_update_comment_check"}
# )

# urlpatterns = [
#     path(
#         "checks/simple/<uuid:check_id>", patch_simple_check, name="patch_simple_check"
#     ),
#     path("checks/date/<uuid:check_id>", patch_date_check, name="patch_date_check"),
#     path(
#         "checks/duration/<uuid:check_id>",
#         patch_duration_check,
#         name="patch_duration_check",
#     ),
#     path(
#         "checks/location/<uuid:check_id>",
#         patch_location_check,
#         name="patch_location_check",
#     ),
#     path(
#         "checks/camp_location/<uuid:check_id>",
#         patch_camp_location_check,
#         name="patch_camp_location_check",
#     ),
#     path(
#         "checks/participant/<uuid:check_id>", patch_participant_check, name="patch_participant_check"
#     ),
#     path(
#         "checks/file/<uuid:check_id>",
#         patch_file_upload_check,
#         name="patch_file_upload_check",
#     ),
#     path(
#         "checks/comment/<uuid:check_id>",
#         patch_comment_check,
#         name="patch_comment_check",
#     ),
# ]


router = routers.SimpleRouter()

# router.register(r"categories", CategoryViewSet, "categories")
# router.register(r"sub_categories", SubCategoryViewSet, "sub_categories")
# router.register(r"category_sets", CategorySetViewSet, "category_sets")
# router.register(r"visums", CampVisumViewSet, "visums")
# router.register(r"checks", LinkedCheckViewSet, "checks")

urlpatterns = router.urls
