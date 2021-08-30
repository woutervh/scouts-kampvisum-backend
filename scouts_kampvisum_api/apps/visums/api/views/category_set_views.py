
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_yasg2.utils import swagger_auto_schema

from ..serializers import CampVisumCategorySetSerializer


class CampVisumCategorySetViewSet(viewsets.GenericViewSet):

    @action(
        detail=False, methods=['get'], permission_classes=[IsAuthenticated],
        url_path='import')
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: CampVisumCategorySetSerializer},
    )
    def sub_categories(self, request):
        pass
