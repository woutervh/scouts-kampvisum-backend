from django.urls import path
from rest_framework import routers

from scouts_auth.inuits.views import (
    PersistedFileViewSet,
    S3FileViewSet,
)

get_presigned_url = S3FileViewSet.as_view({"get": "get_presigned_url"})

urlpatterns = [
    path("files/s3/presigned_url", get_presigned_url, name="get_presigned_url"),
]

router = routers.SimpleRouter()

router.register(r"files", PersistedFileViewSet, "files")

urlpatterns += router.urls
