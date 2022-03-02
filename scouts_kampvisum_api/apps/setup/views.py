from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg2.utils import swagger_auto_schema

from apps.setup.models import Setup, SetupSerializer


import logging

logger = logging.getLogger(__name__)


class SetupViewSet(viewsets.GenericViewSet):
    """
    A viewset for handling basic application setup.
    """

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="setup",
    )
    @swagger_auto_schema(responses={status.HTTP_200_OK: SetupSerializer})
    def check(self, request):
        """
        Returns a simple JSON list that describes the initial data status.
        """

        instance = Setup()
        serializer = SetupSerializer(instance, context={"request": request})

        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="setup/init",
    )
    @swagger_auto_schema(responses={status.HTTP_200_OK: SetupSerializer})
    def init(self, request):
        """
        Returns a simple JSON list that describes the initial data status.
        """
        instance = Setup()

        instance.perform_init(request)

        serializer = SetupSerializer(instance, context={"request": request})

        return Response(serializer.data)
