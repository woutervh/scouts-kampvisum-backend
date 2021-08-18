from rest_framework import routers

from .views import GroupAdminGroupViewSet


router = routers.SimpleRouter()

router.register(r'groupadmin', GroupAdminGroupViewSet, 'groupadmin')

urlpatterns = router.urls