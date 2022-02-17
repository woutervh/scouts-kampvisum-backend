from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path("", include("scouts_auth.auth.urls")),
    path("", include("scouts_auth.groupadmin.urls")),
    path("", include("scouts_auth.inuits.urls")),
]
