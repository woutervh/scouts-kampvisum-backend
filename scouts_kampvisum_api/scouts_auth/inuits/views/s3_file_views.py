from types import SimpleNamespace

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.openapi import Schema, TYPE_STRING

from scouts_auth.inuits.files.aws import S3StorageService
from scouts_auth.inuits.serializers import S3FileSerializer, S3PresignedUrlFileSerializer

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger
from apps.visums.models import LinkedCheck

logger: InuitsLogger = logging.getLogger(__name__)


class S3FileViewSet(viewsets.ViewSet):

    """
    A viewset for viewing and editing PersistedFile instances.
    """
    s3_file_service = S3StorageService()

    @swagger_auto_schema(responses={status.HTTP_200_OK: S3PresignedUrlFileSerializer})
    @action(
        methods=["GET"],
        url_path="",
        detail=False,
    )
    def get_presigned_url(self, request):
        """
        Returns an S3 presigned url
        """

        input_serializer = S3FileSerializer(
            data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("PERSISTED FILE CREATE VALIDATED DATA: %s",
                     validated_data)

        presigned_url = self.s3_file_service.generate_presigned_url(
            validated_data.get("name"))
        serializer = S3PresignedUrlFileSerializer(
            SimpleNamespace(presigned_url=presigned_url), context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: S3PresignedUrlFileSerializer})
    @action(
        methods=["GET"],
        url_path="",
        detail=False,
    )
    def get_presigned_url_post(self, request):
        """
        Returns an S3 presigned url
        """

        input_serializer = S3FileSerializer(
            data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("PERSISTED FILE CREATE VALIDATED DATA: %s",
                     validated_data)

        presigned_url = self.s3_file_service.generate_presigned_url_post(
            validated_data.get("name"))
        serializer = S3PresignedUrlFileSerializer(
            SimpleNamespace(presigned_url=presigned_url), context={"request": request})

        return Response(serializer.data)
