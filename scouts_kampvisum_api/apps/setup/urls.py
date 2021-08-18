from rest_framework import routers

from .views import SetupViewSet


router = routers.SimpleRouter()

router.register(r'', SetupViewSet, 'setup')

urlpatterns = router.urls