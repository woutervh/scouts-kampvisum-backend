"""scouts_kampvisum_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path
from rest_framework import permissions
from drf_yasg2 import openapi
from drf_yasg2.views import get_schema_view

# Open api schema
schema_view = get_schema_view(
    openapi.Info(
        title='Scouts kampvisum API',
        default_version='v1',
        description='This is the api documentation for the Scouts kampvisum API',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    path('api/', include('scouts_auth.urls')),
    path('api/', include('apps.scouts_camps.urls')),
    path('api/', include('apps.scouts_groups.urls')),
    path('api/docs/',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('swagger/',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
]

