from django.urls import path
from rest_framework import routers

from apps.people.views import (
    MemberViewSet,
    NonMemberViewSet,
    PeopleViewSet,
)

urlpatterns = [
    path(
        "members/ga/<str:group_admin_id>",
        MemberViewSet.as_view({"get": "retrieve_scouts_member"}),
    ),
    path("members/ga/", MemberViewSet.as_view({"get": "list_scouts_member"})),
]

router = routers.SimpleRouter()

router.register(r"members", MemberViewSet, "members")
router.register(r"non_members", NonMemberViewSet, "non_members")
router.register(r"people", PeopleViewSet, "people")

urlpatterns += router.urls
