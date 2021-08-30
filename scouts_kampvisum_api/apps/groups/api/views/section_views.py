import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from ..models import Section
from ..serializers import SectionSerializer


logger = logging.getLogger(__name__)


class SectionViewSet(viewsets.GenericViewSet):

    serializer_class = SectionSerializer
    queryset = Section.objects.all()

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: SectionSerializer}
    )
    def list(self, request):
        """
        Retrieves a list of all existing Section instances.
        """

        instances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = SectionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = SectionSerializer(instances, many=True)
            return Response(serializer.data)
