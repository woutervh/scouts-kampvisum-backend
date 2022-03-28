from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from apps.visums.models import CampVisumApproval
from apps.visums.serializers import CampVisumApprovalSerializer
from apps.visums.services import CampVisumApprovalService


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampVisumApprovalViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing and editing camp instances.
    """

    serializer_class = CampVisumApprovalSerializer
    queryset = CampVisumApproval.objects.all()

    camp_visum_approval_service = CampVisumApprovalService()

    @swagger_auto_schema(responses={status.HTTP_200_OK: CampVisumApprovalSerializer})
    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = CampVisumApprovalSerializer(instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CampVisumApprovalSerializer,
        responses={status.HTTP_200_OK: CampVisumApprovalSerializer},
    )
    def partial_update(self, request, pk=None):
        instance = self.get_object()

        logger.debug("CAMP VISUM APPROVAL UPDATE REQUEST DATA: %s", request.data)

        serializer = CampVisumApprovalSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("CAMP VISUM APPROVAL UPDATE VALIDATED DATA: %s", validated_data)

        updated_instance = self.camp_visum_approval_service.update_approval(
            request, instance=instance, **validated_data
        )

        output_serializer = CampVisumApprovalSerializer(
            updated_instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)
