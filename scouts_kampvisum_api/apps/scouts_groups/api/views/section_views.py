import logging
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.openapi import Schema, TYPE_STRING

from ..models import ScoutsSection
from ..serializers import ScoutsSectionSerializer


logger = logging.getLogger(__name__)


class ScoutsSectionViewSet(viewsets.GenericViewSet):

    serializer_class = ScoutsSectionSerializer
    queryset = ScoutsSection.objects.all()

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: ScoutsSectionSerializer}
    )
    def list(self, request):
        """
        Retrieves a list of all existing ScoutsSection instances.
        """
        
        instances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = ScoutsSectionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = ScoutsSectionSerializer(instances, many=True)
            return Response(serializer.data)

