from django.urls import path
from rest_framework import routers

from scouts_auth.inuits.views import (
    PersistedFileViewSet,
    S3FileViewSet,
)

get_presigned_url = S3FileViewSet.as_view({"get": "get_presigned_url"})
get_presigned_url_post = S3FileViewSet.as_view(
    {"post": "get_presigned_url_post"})

urlpatterns = [
    path("files/s3/presigned_url", get_presigned_url, name="get_presigned_url"),
    path("files/s3/presigned_url_post",
         get_presigned_url_post, name="get_presigned_url_post")
]

router = routers.SimpleRouter()

router.register(r"files", PersistedFileViewSet, "files")

urlpatterns += router.urls
