from django.urls import path
from rest_framework import routers

from scouts_auth.inuits.views import (
    PersistedFileViewSet,
)

router = routers.SimpleRouter()
router.register("files", PersistedFileViewSet, "files")

urlpatterns = router.urls
