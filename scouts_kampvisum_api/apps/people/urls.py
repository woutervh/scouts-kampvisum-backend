from rest_framework import routers

from apps.people.views import (
    MemberViewSet,
    NonMemberViewSet,
    PeopleViewSet,
)


router = routers.SimpleRouter()

router.register(r"members", MemberViewSet, "members")
router.register(r"non_members", NonMemberViewSet, "non_members")
router.register(r"people", PeopleViewSet, "people")

urlpatterns = router.urls
